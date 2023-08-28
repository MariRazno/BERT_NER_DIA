import os
import pandas as pd
from transformers import BertForTokenClassification, BertTokenizer
from torch import cuda
from transformers import pipeline
from tqdm import tqdm
import time

from text_cleaning import text_preparation, get_sents



class MyBertModel:
    def __init__(self):

        # define computational resources
        self.device = 'cuda' if cuda.is_available() else 'cpu'
        print(f'Device: {self.device}')

        # loading BERT model
        model_path = os.environ.get('MY_BERT_MODEL_PATH', 'default_model_path')

        # defining the names of word labels
        self.label2id = {'<B_DIA>':2, '<I_DIA>':1, '<O>':0}
        self.id2label = {0:'<O>', 1:'<I_DIA>', 2: '<B_DIA>'}

        if not os.path.exists(model_path):
            print(f"Model not found at {model_path}. Put the correct path to the model.")
        else:

            print(f'Model found at {model_path}')
            print('BERT MODEL loading...')
            self.model = BertForTokenClassification.from_pretrained(model_path)
            self.tokenizer = BertTokenizer.from_pretrained("smanjil/German-MedBERT")

        # pipe will use gpu if device == cuda
        self.pipe = pipeline(task="token-classification", model=self.model.to(self.device), tokenizer=self.tokenizer, aggregation_strategy="simple", device=self.device)

        # path to data in CSV format
        self.data_path = os.environ.get('DATA_PATH', 'data_path')
        self.reports = pd.read_csv(self.data_path)

        # path to save folder
        self.save_folder_path = os.environ.get('SAVE_FOLDER_PATH', 'save_folder_path')
        os.makedirs(self.save_folder_path, exist_ok=True)


    def saver(self, result_list, count):
        df_result = pd.DataFrame(result_list, columns=['nummer', 'report', 'main_diagnoses', 'all_diagnoses', 'probabilities'])
        save_path = f'{self.save_folder_path}/BERT_prediction_{count}_part.csv'

        print(f'Prediction results saved to {save_path}')
        df_result.to_csv(save_path, index=False)
        return [], count+1


    def prediction(self, sentence):
        pred_words = []

        main_dia = ''
        all_dia = ''
        prediction = self.pipe(sentence)

        for elem in prediction:
            if elem['entity_group'] != '<O>':
                if elem['score'] >= 0.80:
                    if elem['entity_group'] == '<I_DIA>':
                        main_dia += ' '+elem['word']
                    else:
                        main_dia += '\n'+elem['word']
                if elem['entity_group'] == '<I_DIA>':
                    all_dia += ' '+elem['word']
                else:
                    all_dia += '\n'+elem['word']
                pred_words.append([elem['word'], elem['entity_group'], round(elem['score'],3)])
        return [main_dia, all_dia, pred_words]


    def df_processing(self):
        print(f'YOU PASSED {len(self.reports)} REPORTS \nSAVING RESULT EACH 100 REPORTS')

        save_interval = 100
        count = 1

        # list with model's predictions
        result_list = []

        with tqdm(total=len(self.reports)) as pbar:
            for ind, elem in self.reports.iterrows():

                # list with model's predictions for each report
                report_list = [elem['nummer']]

                # raw report
                report = elem['report']

                #cleaning report
                clean_report = text_preparation(report)

                # get report sents
                report_sents = get_sents(clean_report)
                report_list.append(' '.join(report_sents))

                # run prediction function
                main_dia = ''
                all_dia = ''
                probabilities = []

                for sent in report_sents:
                    pred = self.prediction(sent)
                    main_dia += pred[0]
                    all_dia += pred[1]
                    probabilities.append(pred[2])

                report_list.extend([main_dia, all_dia, probabilities])

                # adding report predictions to the general list
                result_list.append(report_list)
                pbar.update()

                if len(result_list) == save_interval:
                    result_list, count = self.saver(result_list, count)


            result_list, count = self.saver(result_list, count)




if __name__ == "__main__":
    start_time = time.time()

    processing = MyBertModel()
    processing.df_processing()
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Execution time: {execution_time:.2f} seconds")


# coding=utf-8
"""
Módulo de treinamento.
"""
import os

import cv2 as cv
import numpy as np
from PIL import Image

import settings
from core.abstract_middleware import BaseMiddleware
from core.utils import RecognizerType


class FaceTraining(BaseMiddleware):
    """ Treinamento de Faces. """

    def __init__(self, path, next_middleware=None, verbose=True, sep='_'):
        super(FaceTraining, self).__init__(next_middleware)
        self._sep = sep
        self._verbose = verbose
        self._path = os.path.normpath(path)
        self._files = []
        self._faces = []
        self._ids = []

    def _load_data(self):
        """ Carrega os dados de ids e imagens. """
        if self._verbose:
            print('Carregando os dados...')
        self._files = [os.path.join(self._path, f) for f in os.listdir(self._path)]
        self._faces = []
        self._ids = []
        if self._files:
            for path in self._files:
                if self._verbose:
                    print(f'Carregando o arquivo {path}...')
                # Carrega a face para treino.
                self._faces.append(cv.cvtColor(cv.imread(path), cv.COLOR_BGR2GRAY))
                # Carrega o ID para treino.
                self._ids.append(self._get_ids_from_file(path))
        self._ids = np.array(self._ids)
        return self

    def _get_ids_from_file(self, path):
        """ Recupera os Ids através dos nomes dos arquivos. """
        return int(os.path.split(path)[-1].split(self._sep)[1])

    @staticmethod
    def _new_recognizer(recognizer_type):
        """ Recupera o recognizer. """
        result = recognizer_type.new_recognizer(**{
            RecognizerType.EIGEN: {'num_components': 40, 'threshold': 8000},
            RecognizerType.FISHER: {'num_components': 3, 'threshold': 2000},
            RecognizerType.LBPH: {'radius': 2, 'neighbors': 2, 'grid_x': 7, 'grid_y': 7, 'threshold': 50}
        }[recognizer_type])
        return result

    def _fit(self, pos_id=''):
        """ Executar o treinamento dos dados. """
        if self._verbose:
            print('treinando...')
        for recognizer in RecognizerType:
            # Recupera o classificador.
            c = self._new_recognizer(recognizer)
            c.train(src=self._faces, labels=self._ids)
            c.write(os.path.join(settings.BASE_DIR + '/data/training', f'{recognizer.value[1] + pos_id}.yml'))
            if self._verbose:
                print(f'Treinamento {recognizer.value[1]} executado com sucesso...')
        if self._verbose:
            print('Treinamento realizado com sucesso...')
        return self

    def fit(self):
        """ Execução completa do treinamento. """
        self._load_data()._fit()
        return self

    def _process(self, frame):
        """ Executa o processamento do treino. """
        return frame


class FaceTrainingYale(FaceTraining):
    """ Treinamento Yale. """

    def _load_data(self):
        """ Carrega os dados de ids e imagens. """
        if self._verbose:
            print('Carregando os dados...')
        self._files = [os.path.join(self._path, f) for f in os.listdir(self._path)]
        self._faces = []
        self._ids = []
        if self._files:
            for path in self._files:
                if self._verbose:
                    print(f'Carregando o arquivo {path}...')
                # Carrega a face para treino.
                self._faces.append(np.array(Image.open(path).convert('L'), 'uint8'))
                # Carrega o ID para treino.
                self._ids.append(self._get_ids_from_file(path))
        self._ids = np.array(self._ids)
        return self

    def _get_ids_from_file(self, path):
        """ Recupera os Ids através dos nomes dos arquivos. """
        return int(os.path.split(path)[1].split('.')[0].replace('subject', ''))

    @staticmethod
    def _new_recognizer(recognizer_type):
        """ Recupera o recognizer. """
        result = recognizer_type.new_recognizer(**{
            RecognizerType.EIGEN: {'num_components': 40, 'threshold': 8000},
            RecognizerType.FISHER: {'num_components': 3, 'threshold': 2000},
            RecognizerType.LBPH: {'radius': 2, 'neighbors': 2, 'grid_x': 7, 'grid_y': 7, 'threshold': 50}
        }[recognizer_type])
        return result

    def fit(self):
        """ Execução completa do treinamento. """
        self._load_data()._fit(pos_id='Yale')
        return self


def main():
    """ Método de teste. """
    FaceTraining(path=settings.BASE_DIR + '/data/photos').fit()
    # FaceTrainingYale(path=settings.BASE_DIR + '/data/photos').fit()


if __name__ == '__main__':
    main()

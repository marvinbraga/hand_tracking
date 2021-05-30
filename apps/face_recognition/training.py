# coding=utf-8
"""
Módulo de treinamento.
"""
import os
from enum import Enum

import cv2 as cv
import numpy as np

import settings
from core.abstract_middleware import BaseMiddleware


class RecognizerType(Enum):
    """ Tipos de reconhecedores. """
    EIGEN = 0, 'EigenFace'
    FISHER = 1, 'FisherFace'
    LBPH = 2, 'LBPHFace'

    def new_recognizer(self):
        """ Factory Method para Recognizer. """
        result = {
            RecognizerType.EIGEN: cv.face.EigenFaceRecognizer_create,
            RecognizerType.FISHER: cv.face.FisherFaceRecognizer_create,
            RecognizerType.LBPH: cv.face.LBPHFaceRecognizer_create
        }[self]
        return result()


class FaceTraining(BaseMiddleware):
    """ Treinamento de Faces. """

    def __init__(self, path, next_middleware=None, verbose=True):
        super(FaceTraining, self).__init__(next_middleware)
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
                self._ids.append(int(os.path.split(path)[-1].split('_')[1]))
        self._ids = np.array(self._ids)
        return self

    def _fit(self):
        """ Executar o treinamento dos dados. """
        if self._verbose:
            print('treinando...')
        for recognizer in RecognizerType:
            c = recognizer.new_recognizer()
            c.train(src=self._faces, labels=self._ids)
            c.write(os.path.join(settings.BASE_DIR + '/data/training', f'{recognizer.value[1]}.yml'))
            if self._verbose:
                print(f'Treinamento {recognizer.value[1]} executado com sucesso...')
        if self._verbose:
            print('Treinamento realizado com sucesso...')
        return self

    def fit(self):
        """ Execução completa do treinamento. """
        self._load_data()._fit()

    def _process(self, frame):
        """ Executa o processamento do treino. """
        return frame


def main():
    """ Método de teste. """
    FaceTraining(path=settings.BASE_DIR + '/data/photos').fit()


if __name__ == '__main__':
    main()

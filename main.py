from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
import time
from collections import Counter
import argparse
from pathlib import Path

class ImageRecon:

    def __init__(self, img):
        self.img = img

    def populate_array(self):
        i = Image.open(self.img)
        image_array = np.asarray(i)
        return image_array

    @staticmethod
    def create_example():
        numberArrayExamples = open('numArEx.txt','a')
        numbersWeHave = range(1,10)
        for eachNum in numbersWeHave:
            for furtherNum in numbersWeHave:
                imgFilePath = 'images/numbers/'+str(eachNum)+'.'+str(furtherNum)+'.png'
                ei = Image.open(imgFilePath)
                eiar = np.array(ei)
                eiarl = str(eiar.tolist())
                lineToWrite = str(eachNum)+'::'+eiarl+'\n'
                numberArrayExamples.write(lineToWrite)

    def threshold(self):
        balance_array = []
        new_array = self.populate_array()
        #making array writable
        new_array.setflags(write=1)

        for each_row in self.populate_array():
            for each_pixel in each_row:
                avg_number = mean(each_pixel[:3])
                balance_array.append(avg_number)

        balance = mean(balance_array)

        for each_row in new_array:
            for each_pixel in each_row:
                if mean(each_pixel[:3]) > balance:
                    each_pixel[0] = 255
                    each_pixel[1] = 255
                    each_pixel[2] = 255
                    each_pixel[3] = 255
                else:
                    each_pixel[0] = 0
                    each_pixel[1] = 0
                    each_pixel[2] = 0
                    each_pixel[3] = 255
        return new_array

    def identify(self):
        matchedAr = []
        loadExamps = open('numArEx.txt','r').read()
        loadExamps = loadExamps.split('\n')
        i = Image.open(self.img)
        iar = np.array(i)
        iarl = iar.tolist()
        inQuestion = str(iarl)
        for eachExample in loadExamps:
            try:
                splitEx = eachExample.split('::')
                currentNum = splitEx[0]
                currentAr = splitEx[1]
                eachPixEx = currentAr.split('],')
                eachPixInQ = inQuestion.split('],')
                x = 0
                while x < len(eachPixEx):
                    if eachPixEx[x] == eachPixInQ[x]:
                        matchedAr.append(int(currentNum))

                    x+=1
            except Exception as e:
                print(str(e))
        x = Counter(matchedAr)
        print(x)
        graphX = []
        graphY = []

        ylimi = 0

        for eachThing in x:
            graphX.append(eachThing)
            graphY.append(x[eachThing])
            ylimi = x[eachThing]

        fig = plt.figure()
        ax1 = plt.subplot2grid((4,4),(0,0), rowspan=1, colspan=4)
        ax2 = plt.subplot2grid((4,4),(1,0), rowspan=3,colspan=4)

        ax1.imshow(iar)
        ax2.bar(graphX,graphY,align='center')
        plt.ylim(400)
        xloc = plt.MaxNLocator(12)
        ax2.xaxis.set_major_locator(xloc)
        plt.show()

def main():
    parser = argparse.ArgumentParser(description='Identifying images based on datasets.')
    parser.add_argument('image_path', metavar='-p', type=str, help='Image path for Comparison')
    args = parser.parse_args()
    ir = ImageRecon(args.image_path)
    my_file = Path("numArEx.txt")
    if not my_file.is_file():
        ir.create_example()
    else:
        ir.identify()


if __name__ == '__main__':
    main()
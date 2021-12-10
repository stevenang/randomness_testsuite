# NIST Randomness Testsuit

This is a Python implementation of NIST's A Statistical Test Suite for Random and Pseudorandom Number Generators for Cryptographic Applications

## Getting Started

### Prerequisite:
You need the following software and packages for this application:
1. Python 3.6 and above (Tested with Python 3.8 already)
2. Numpy and Scipy
```
pip3 install numpy, scipy
```

### How to use:
* You can start the program using your IDE feature (like run) to run Main.py or 
```
    python3 Main.py
```
* Once you saw the interface, you can start using the test suite.
![Test Suite Screenshot](https://user-images.githubusercontent.com/25377399/145481469-183b14c3-cad8-4a8b-a841-7d45a09714a8.png)

    * Input Data - Input Data contains Binary Data, Binary Data File and String Data File
    * Binary Data - You can only enter a BINARY STRING here (ex:1100100100001111110110101010001000100001011010001100001000110100110001001100011001100010100010111000)
    * Binary Data File - This will open a file dialog where you can select a file to be read by program.
                       The file you selected should contain only one set of data in BINARY FORM.  (For example, please refer to data/data.e)
    * String Data File - This will open a file dialog where you can select a file to be read by program.
                       The file you selected can contain multiple set of data in STRING FORM.  (For example, please refer to data/test_data_01.txt)

* You can select the type of test you want to perform by clicking the corresponding checkbox or press "Select All Test" to select everything
* You can cancel the selection by clicking the corresponding checkbox or press "De-Select All Test" to cancel everything
* Once you have your data ready and selected the test you want to perform, then you can press "Execute Test" button to execute the test
* The result will be displayed after the test done.
    * There are multiple result for Random Excursion Test.  Initially the program will displayed state '+1'.  You can chechk the other resuld
         by changing the state (using drop down) and press "Update" button
    * There are multiple result for Random Excursion Variant Test.  Initially the program will displayed state '-1.0'.  You can chechk the other resuld
         by changing the state (using drop down) and press "Update" button
* You can save the result to a text file by pressing "Save as Text File" button.
    This will display a file dialog where you can enter the file name for your result.
    You can check the text file after the result is saved.
* "Reset" button will clear all input and variables.  It is strongly suggested you use this feature if you want to execute test for another set of data
* "Exit" button will close this program

### Using this application in terminal (Command Line)
* You can also used this application by importing necessary library to your python code
```
import os
from FrequencyTest import FrequencyTest
from RunTest import RunTest
from Matrix import Matrix
from Spectral import SpectralTest
from TemplateMatching import TemplateMatching
from Universal import Universal
from Complexity import ComplexityTest
from Serial import Serial
from ApproximateEntropy import ApproximateEntropy
from CumulativeSum import CumulativeSums
from RandomExcursions import RandomExcursions

# Open Data File and read the binary data of e
data_path = os.path.join(os.getcwd(), 'data', 'data.e')
handle = open(data_path)
data_list = []

for line in handle:
    data_list.append(line.strip().rstrip())

binary_data = ''.join(data_list)

print('The statistical test of the Binary Expansion of e')
print('2.01. Frequency Test:\t\t\t\t\t\t\t\t', FrequencyTest.monobit_test(binary_data[:1000000]))
print('2.02. Block Frequency Test:\t\t\t\t\t\t\t', FrequencyTest.block_frequency(binary_data[:1000000]))
print('2.03. Run Test:\t\t\t\t\t\t\t\t\t\t', RunTest.run_test(binary_data[:1000000]))
print('2.04. Run Test (Longest Run of Ones): \t\t\t\t', RunTest.longest_one_block_test(binary_data[:1000000]))
print('2.05. Binary Matrix Rank Test:\t\t\t\t\t\t', Matrix.binary_matrix_rank_text(binary_data[:1000000]))
print('2.06. Discrete Fourier Transform (Spectral) Test:\t', SpectralTest.spectral_test(binary_data[:1000000]))
print('2.07. Non-overlapping Template Matching Test:\t\t', TemplateMatching.non_overlapping_test(binary_data[:1000000], '000000001'))
print('2.08. Overlappong Template Matching Test: \t\t\t', TemplateMatching.overlapping_patterns(binary_data[:1000000]))
print('2.09. Universal Statistical Test:\t\t\t\t\t', Universal.statistical_test(binary_data[:1000000]))
print('2.10. Linear Complexity Test:\t\t\t\t\t\t', ComplexityTest.linear_complexity_test(binary_data[:1000000]))
print('2.11. Serial Test:\t\t\t\t\t\t\t\t\t', Serial.serial_test(binary_data[:1000000]))
print('2.12. Approximate Entropy Test:\t\t\t\t\t\t', ApproximateEntropy.approximate_entropy_test(binary_data[:1000000]))
print('2.13. Cumulative Sums (Forward):\t\t\t\t\t', CumulativeSums.cumulative_sums_test(binary_data[:1000000], 0))
print('2.13. Cumulative Sums (Backward):\t\t\t\t\t', CumulativeSums.cumulative_sums_test(binary_data[:1000000], 1))
result = RandomExcursions.random_excursions_test(binary_data[:1000000])
print('2.14. Random Excursion Test:')
print('\t\t STATE \t\t\t xObs \t\t\t\t P-Value \t\t\t Conclusion')

for item in result:
    print('\t\t', repr(item[0]).rjust(4), '\t\t', item[2], '\t\t', repr(item[3]).ljust(14), '\t\t',
          (item[4] >= 0.01))

result = RandomExcursions.variant_test(binary_data[:1000000])

print('2.15. Random Excursion Variant Test:\t\t\t\t\t\t')
print('\t\t STATE \t\t COUNTS \t\t\t P-Value \t\t Conclusion')
for item in result:
    print('\t\t', repr(item[0]).rjust(4), '\t\t', item[2], '\t\t', repr(item[3]).ljust(14), '\t\t',
          (item[4] >= 0.01))
```
* Output of the code above:
```
The statistical test of the Binary Expansion of e
2.01. Frequency Test:								 (0.9537486285283232, True)
2.02. Block Frequency Test:							 (0.21107154370164066, True)
2.03. Run Test:										 (0.5619168850302545, True)
2.04. Run Test (Longest Run of Ones): 				 (0.7189453298987654, True)
2.05. Binary Matrix Rank Test:						 (0.3061558375306767, True)
2.06. Discrete Fourier Transform (Spectral) Test:	 (0.8471867050687718, True)
Non-Overlapping Template Test DEBUG BEGIN:
	Length of input:		 1000000
	Value of Mean (µ):		 244.125
	Value of Variance(σ):	 236.03439331054688
	Value of W:				 [239. 235. 254. 278. 207. 229. 225. 242.]
	Value of xObs:			 14.116057212121211
	P-Value:				 0.07879013267666338
DEBUG END.
2.07. Non-overlapping Template Matching Test:		 (0.07879013267666338, True)
2.08. Overlappong Template Matching Test: 			 (0.11043368541387631, True)
2.09. Universal Statistical Test:					 (0.282567947825744, True)
2.10. Linear Complexity Test:						 (0.8263347704038304, True)
2.11. Serial Test:									 ((0.766181646833394, True), (0.46292132409575854, True))
2.12. Approximate Entropy Test:						 (0.7000733881151612, True)
2.13. Cumulative Sums (Forward):					 (0.6698864641681423, True)
2.13. Cumulative Sums (Backward):					 (0.7242653099698069, True)
2.14. Random Excursion Test:
		 STATE 			 xObs 				 P-Value 			 Conclusion
		 '-4' 		 3.8356982129929085 		 0.5733056949947805 		 True
		 '-3' 		 7.318707114093956 		 0.19799602021827734 		 True
		 '-2' 		 7.861927251636425 		 0.16401104937943733 		 True
		 '-1' 		 15.69261744966443 		 0.007778723096466819 		 False
		 '+1' 		 2.4308724832214765 		 0.7868679051783156 		 True
		 '+2' 		 4.7989062888391745 		 0.44091173664620265 		 True
		 '+3' 		 2.3570405369127525 		 0.7978539716877826 		 True
		 '+4' 		 2.4887672641992014 		 0.7781857852321322 		 True
2.15. Random Excursion Variant Test:						
		 STATE 		 COUNTS 			 P-Value 		 Conclusion
		 '-9.0' 		 1450 		 0.8589457398254003 		 True
		 '-8.0' 		 1435 		 0.7947549562546549 		 True
		 '-7.0' 		 1380 		 0.5762486184682754 		 True
		 '-6.0' 		 1366 		 0.4934169340861271 		 True
		 '-5.0' 		 1412 		 0.6338726691411485 		 True
		 '-4.0' 		 1475 		 0.9172831477915963 		 True
		 '-3.0' 		 1480 		 0.9347077918349618 		 True
		 '-2.0' 		 1468 		 0.8160120366175745 		 True
		 '-1.0' 		 1502 		 0.8260090128330382 		 True
		 '+1.0' 		 1409 		 0.13786060890864768 		 True
		 '+2.0' 		 1369 		 0.20064191385523023 		 True
		 '+3.0' 		 1396 		 0.4412536221564536 		 True
		 '+4.0' 		 1479 		 0.939290606067626 		 True
		 '+5.0' 		 1599 		 0.5056826821687638 		 True
		 '+6.0' 		 1628 		 0.4459347106499899 		 True
		 '+7.0' 		 1619 		 0.5122068856164792 		 True
		 '+8.0' 		 1620 		 0.5386346977772863 		 True
		 '+9.0' 		 1610 		 0.5939303958223099 		 True

Process finished with exit code 0
```
* For more example, you can check test_pi.py, test_sqrt2.py, test_sqrt3.py

## Change logs
### 1.3
   * Changed screen layout to fixedthe issue with the resolution lower than 1920 x 1080 
### 1.2
   * Fixed bug
### 1.1
   * Initial Release

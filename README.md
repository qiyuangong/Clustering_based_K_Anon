Clustering Based k-Anonymization
===========================

This repository is an **open source python implementation for Clustering based k-Anonymization**. I implement this algorithm in python for further study.

### Motivation 
Researches on data privacy have lasted for more than ten years, lots of great papers have been published. However, only a few open source projects are available on Internet [3-4], most open source projects are using algorithms proposed before 2004! Fewer projects have been used in real life. Worse more, most people even don't hear about it. Such a tragedy! 

I decided to make some effort. Hoping these open source repositories can help researchers and developers on data privacy (privacy preserving data publishing).

### Attention
I used **both adult and INFORMS** dataset in this implementation. For clarification, **we transform NCP to percentage**. This NCP percentage is computed by dividing NCP value with the number of values in dataset (also called GCP[5]). The range of NCP percentage is from 0 to 1, where 0 means no information loss, 1 means loses all information (more meaningful than raw NCP, which is sensitive to size of dataset). 


### Usage and Parameters:
My Implementation is based on Python 2.7 (not Python 3.0). Please make sure your Python environment is collectly installed. You can run Mondrian in following steps: 

1) Download (or clone) the whole project. 

2) Run `anonymized.py` in root dir with CLI.

Parameters:

	#Usage: python anonymizer [a | i] [knn | kmember | oka] [k | qi | data]
	#a: adult dataset, i: INFORMS ataset
	#knn:k-nearest neighbor, kmember: k-member, oka: one time pass k-means algorithm
	#k: varying k, qi: varying qi numbers, data: varying size of dataset
	# run Mondrian with adult data and oka with K(K=10)
	python anonymizer.py a oka 10
	
	# evalution knn by varying k
	python anonymized.py a knn k


### For more information:
[1] K. LeFevre, D. J. DeWitt, R. Ramakrishnan. Mondrian Multidimensional K-Anonymity ICDE '06: Proceedings of the 22nd International Conference on Data Engineering, IEEE Computer Society, 2006, 25

[2] K. LeFevre, D. J. DeWitt, R. Ramakrishnan. Workload-aware Anonymization. Proceedings of the 12th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, ACM, 2006, 277-286

[3] [UTD Anonymization Toolbox](http://cs.utdallas.edu/dspl/cgi-bin/toolbox/index.php?go=home)

[4] [ARX- Powerful Data Anonymization](https://github.com/arx-deidentifier/arx)

[5] G. Ghinita, P. Karras, P. Kalnis, N. Mamoulis. Fast data anonymization with low information loss. Proceedings of the 33rd international conference on Very large data bases, VLDB Endowment, 2007, 758-769

==========================
by Qiyuan Gong
qiyuangong@gmail.com

2016-1-27
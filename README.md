# FishID
This project was focused on building a machine learning model that is capable of identifying what species of fish is present in a given image. This however turned out to be much more complicated than simply training a CNN. At a high level the process for this project:

1. Scrape Hawaiian fish species information and images from fishbase ([Data_Sourcing.ipynb](https://github.com/syellamilli/FishID/blob/master/Data_Sourcing.ipynb))
2. Scrape additional images for each species from google images using selenium ([Augmenting_Species_Data.ipynb](https://github.com/syellamilli/FishID/blob/master/Augmenting_Species_Data.ipynb) and [WebScraping.py](https://github.com/syellamilli/FishID/blob/master/WebScraping.py)) 
3. Build IsFish CNN classifier from fishbase images and mini imagenet to filter out non-fish images from google image results ([Is_Fish_PT.ipynb](https://github.com/syellamilli/FishID/blob/master/Is_Fish_PT.ipynb))
4. Build relevant datasets for each model ([Generate_Datasets.ipynb](https://github.com/syellamilli/FishID/blob/master/Generate_Datasets.ipynb))
5. Perform Experiments to find the best possible species classifier. ([Species_Classifier.ipynb](https://github.com/syellamilli/FishID/blob/master/Species_Classifier.ipynb) and [ExpandedSpeciesClassifier.ipynb](https://github.com/syellamilli/FishID/blob/master/ExpandedSpeciesClassifier.ipynb))

To read about the overall process in more detail, check out my blog post [here](https://syellamilli.github.io/fish_classifier.html); to read about the CNN experiments I conducted, click [here](https://syellamilli.github.io/fc_details.html). If you would like to request access to the models, please reach out to me at shivaramyellamilli@gmail.com.


---
# Citations
This work would not have been possible without the numerous resources I found to help me along the way; I have linked them below.

Models

- [Resnet Paper](https://arxiv.org/abs/1512.03385v1)
- [Efficient Net Paper](https://arxiv.org/abs/1905.11946)
- [Convnet Paper](https://arxiv.org/abs/2201.03545)

Data

- [Fishbase](https://www.fishbase.se/search.php)
- [Mini Imagenet](https://image-net.org/)

Other Coding Resources

- [CNN Tutorial in Pytorch](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
- [Selenium Scraper Tutorial](https://medium.com/geekculture/scraping-images-using-selenium-f35fab26b122)
- [Data Augmentation Paper](https://journalofbigdata.springeropen.com/articles/10.1186/s40537-019-0197-0)
- [Slugify](https://github.com/django/django/blob/master/django/utils/text.py)

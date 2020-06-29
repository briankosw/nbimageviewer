# nbimageviewer

nbimageviewer is a Python library for rapid image visualization in Jupyter Notebooks. It uses IPython, HTML and JavaScript, and WebSockets to efficiently visualize large amounts of images.

Visualizing large amounts of images in a Jupyter Notebook is usually done by creating matplotlib plots, which can be a painful and inefficient process with lots of configuring and searching online.

```
import matplotlib.pyplot as plt
import load_images

images = load_images()
fig, ax = plt.subplots()
for i, image in enumerate(len(images)):
  ax[i] = plt.imshow(image)
  ...
```

nbimageviewer simplifies this process while providing convenient and beautiful visualizations.

```
import nbimageviewer.carousel as carousel
import load_images

images = load_images()
c = carousel.Carousel(images)
```

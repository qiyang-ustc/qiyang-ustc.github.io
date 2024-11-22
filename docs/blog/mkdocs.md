---
title: Why I use mkdocs to build my blog
date: 2024-11-16
---

# Why I use mkdocs to build my blog

In the past, I tried to use Jekyll to build my blog, but I have to admit that I know nothing about Ruby. It is like a mysterious and unfathomable sea, where I could easily get lost. So I decided to take a step back and search for something more familiar to me, something similar to `Python` instead of `Ruby`. That is when I found mkdocs.

I asked Claude, to help me build my blog. Claude told me that mkdocs is a good choice. 


```bash
blog/
├── content/
│   ├── posts/
│   │   └── your-posts.md
│   ├── papers/
│   │   └── pdf-files/
│   └── code/
│       └── demos/
├── static/
│   └── images/
└── notebooks/
    └── jupyter-files/
```

and 

```bash
pip install mkdocs-material
mkdocs new my-blog
cd my-blog
mkdocs serve  # server, reload automatically, I love it!
```

It is fine, and works pretty well.

Also the mathematical formula can also be displayed well.

$$ \frac{d x^*}{d \theta} = (I - \frac{\partial G}{\partial x})^{-1} \frac{\partial G}{\partial \theta} $$


with open(".flake8", "w") as f:
    f.write("[flake8]\nmax-line-length = 200\nextend-ignore = E203, W503, F541\nexclude = .git,__pycache__,docs/source/conf.py,old,build,dist\n")

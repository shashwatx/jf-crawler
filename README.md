**TODO** 
  1. Add section on results. 

# Introduction 
  
Crawls Job Adverts from a Popular Spanish Site using bs4.
    

# License

[MIT](https://github.com/shashwatx/jf-crawler/blob/master/LICENSE)


# Requirements
Package | Version
-----|------|
[coloredlogs](https://pypi.org/project/coloredlogs/)|7.3| Logging
[bs4](https://pypi.org/project/beautifulsoup4/) |4.7.1| HTML Parser
[click](https://pypi.org/project/click/) |7.0| Command line args


# Setup
1. Clone the repo.
```
git clone git@github.com:shashwatx/jf-crawler.git
```
2. Install dependencies
```
pip install -r requirements.txt
```

# Usage

**Generate help**

```
shashwat@homestation ~/repos/jf-crawler $ python jf-crawler.py --help
Usage: jf-crawler.py [OPTIONS]

Options:
-c, --city [madrid|london|paris|amsterdam|berlin|barcelona]
-o, --output TEXT               name of output file
--help                          Show this message and exit.
```

**Example**
```
python jf-crawler.py --city paris -o paris.out
```


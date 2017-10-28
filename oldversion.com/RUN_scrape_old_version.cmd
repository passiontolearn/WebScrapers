:: Thanks to https://stackoverflow.com/a/28827752 
::
:: Note: the "-t" parameter is deprecated so I'm not using it
python -mtimeit -n1 -r1 -s "from scrape_oldversion_exes import main" "main()" > dl_urls.txt
PAUSE
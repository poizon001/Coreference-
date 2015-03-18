import re
numbers = "(^a(?=\s)|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand)"
day = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
week_day = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
month = "(january|february|march|april|may|june|july|august|september|october|november|december|January|February|March|April|May|June|July|August|September|October|November|December)"
month1 = "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
dmy = "(year|week|month|quarter)"
rel_day = "(today|yesterday|tomorrow|tonight|tonite)"
exp1 = "(before|after|earlier|later|ago|past)"
exp2 = "(this|next|last|coming|upcoming|past|mid)"
iso = "\d+[/-]\d+[/-]\d+ \d+:\d+:\d+\.\d+"
year = "((?<=\s)\d{4}|^\d{4})"
patt = "\d{1,2}\s(years|days|week|months|quarters|quarter|month|year|day)"
patt1 = "(first|second|third|fourth)\s(quarters|quarter)"
patt2 = "Q1|Q2|Q3|Q4"
patt3 = "(end of the year|end of this year|end of this week|end pf this month|end of this quarter|second half)"
patt4 = "'[0,1]{1}[0-9]{1}"
regxp1 = "((\d+|(" + numbers + "[-\s]?)+) " + dmy + "s? " + exp1 + ")"
regxp2 = "(" + exp2 + " (" + dmy + "|" + week_day + "|" + month + "))"
reg1 = re.compile(regxp1, re.IGNORECASE)
reg2 = re.compile(regxp2, re.IGNORECASE)
reg3 = re.compile(rel_day, re.IGNORECASE)
reg4 = re.compile(iso)
reg5 = re.compile(year)
patt5 = month + ",\s[1,2]{1}[0,1,2,9]{1}[0-9]{1}[0-9]{1}"  
patt6 = exp2 + "-?\s?[1,2]{1}[0,1,2,9]{1}[0-9]{1}[0-9]{1}" 
patt7 = month + "\s\d+,\s?\s?\s?\s?[1,2]{1}[0,1,2,9]{1}[0-9]{1}[0-9]{1}" 
patt8 = month1 + ".\s\d{2},\s[1,2]{1}[0,1,2,9]{1}[0-9]{1}[0-9]{1}"
patt9 = month + "\s[1,2]{1}[0,1,2,9]{1}[0-9]{1}[0-9]{1}" 
patt10 = month + "\s[0,1,2]{1}[0-9]{1}" 


def tag(text):
    timex_found = []
    flag = 0
    
    m7 = re.finditer(patt7, text)
    m10 = re.finditer(patt10, text)
    m9 = re.finditer(patt9, text)
    m8 = re.finditer(patt8, text)
    m6 = re.finditer(patt6, text)
    m5 = re.finditer(patt5, text)


    if m5:
        for x in m5:
            flag = 1
            timex_found.append(x.group(0))
    elif m7:        
        for x in m7:
            timex_found.append(x.group(0))
            flag = 1
    elif m10:
        for x in m10:
            timex_found.append(x.group(0))
    elif m9:
        for x in m9:
            timex_found.append(x.group(0))

    else:
        found = reg5.findall(text)
        for timex in found:
            timex_found.append(timex)


    for x in m8:
        timex_found.append(x.group(0))


    found = reg4.findall(text)
    for timex in found:
        timex_found.append(timex)

    

    for x in m6:
        timex_found.append(x.group(0))

    m = re.finditer(patt, text)
    for x in m:
        timex_found.append(x.group(0))

    m1 = re.finditer(patt1, text)
    for x in m1:
        timex_found.append(x.group(0))

    m2 = re.finditer(patt2, text)
    for x in m2:
        timex_found.append(x.group(0))

    m3 = re.finditer(patt3, text)
    for x in m3:
        timex_found.append(x.group(0))

    m4 = re.finditer(patt4, text)
    for x in m4:
        timex_found.append(x.group(0))

    found = reg1.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
        timex_found.append(timex)

    found = reg2.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
        timex_found.append(timex)

    found = reg3.findall(text)
    for timex in found:
        timex_found.append(timex)

        
    return timex_found

def extract(text):
    exp = "(next|last|coming|upcoming|past)"
    durs = "(years|days|week|months|quarters|quarter|month|year|day)"
    r8 = exp + "\s(\d*)\s" + durs # Next 120 days

    month = "(january|february|march|april|may|june|july|august|september|october|november|december)"
    # month_s = "(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)"
    month_s = "(sept)"
    year = "((18|19|20)\d{2})"
    date_no = "\d{0,2}(th|st|nd|rd|,)?"
    monthx =  month + "|" + month_s + "(\.)?"

    r1 = "(" + monthx  + ")\s" + date_no + "\s" + year ## Jan 20th 2012 and similar
    r2 = "\d{0,2}(th)?\s("+monthx+")\s((18|19|20)\d{2})" ## 20th Jan 2012 and similar
    r3 = "(" + monthx + ")\s" + date_no ## Jan 10
    r4 =  date_no + "\s(" + monthx + ")" ## 10 Jan
    r5 = year 
    r6 = "(" + monthx + ")" 
    r7 = r6 + "\s" + r5
    r61 = month


    res = []
    
    bigger = False
    if bigger == False:
        m1 = re.finditer(r1, text)
        for x in m1:
            res.append(x.group(0))
            bigger = True

        m2 = re.finditer(r2, text)
        for x in m2:
            res.append(x.group(0))
            bigger = True

    
    m8 = re.finditer(r8, text)
    for x in m8:
        res.append(x.group(0))


    if bigger == False:
        m3 = re.finditer(r3, text)
        for x in m3:
            bigger = True
            res.append(x.group(0))
           

        m4 = re.finditer(r4, text)
        for x in m4:
            res.append(x.group(0))
            bigger = True

    


    if bigger == False:
        m5 = re.finditer(r5, text)
        for x in m5:
            res.append(x.group(0))
            bigger = True

        m6 = re.finditer(r61, text)
        for x in m6:
            res.append(x.group(0))
            bigger = True

    return res





# if __name__ == '__main__':
#     new = []
#     data = open("output3.txt").read().split("\n")
#     for j,line in enumerate(data):
       
#         sent = line.replace(",","").lower()

#         print sent
#         a = tag(sent)
#         b = extract(sent)
#         if a:
#             print a
#         if b:
#             print b
#         print





a = "I may like this in rand august "
a = "Hello october 12, 2014"
print tag(a)
print extract(a)
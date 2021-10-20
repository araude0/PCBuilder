#!D:\Work\Python_workspace\Capstone\venv\Scripts\python.exe
print("content-type:text/html; charset=euc-kr\n")

import pymysql
import pandas as pd
import cgi
#DB접속
db = pymysql.connect(
    user = 'capstonernd',
    passwd = '1q2w3e4r!',
    host = '121.168.135.156',
    db = 'capstone_modules',
    charset = 'utf8'
)
#변수에 DB 테이블을 받아넣음(데이터프레임)
cursor = db.cursor(pymysql.cursors.DictCursor)
sql = "SELECT * FROM capstone_modules.cpu;"
cursor.execute(sql)
cpu = cursor.fetchall()
cpu = pd.DataFrame(cpu)
sql = "SELECT * FROM capstone_modules.mb;"
cursor.execute(sql)
mb = cursor.fetchall()
mb = pd.DataFrame(mb)
sql = "SELECT * FROM capstone_modules.psu;"
cursor.execute(sql)
psu = cursor.fetchall()
psu = pd.DataFrame(psu)
sql = "SELECT * FROM capstone_modules.ram;"
cursor.execute(sql)
ram = cursor.fetchall()
ram = pd.DataFrame(ram)
sql = "SELECT * FROM capstone_modules.vga;"
cursor.execute(sql)
vga = cursor.fetchall()
vga = pd.DataFrame(vga)
sql = "SELECT * FROM capstone_modules.case;"
cursor.execute(sql)
case = cursor.fetchall()
case = pd.DataFrame(case)
sql = "SELECT * FROM capstone_modules.cpucooler;"
cursor.execute(sql)
cpucooler = cursor.fetchall()
cpucooler = pd.DataFrame(cpucooler)
sql = "SELECT * FROM capstone_modules.ssd;"
cursor.execute(sql)
ssd = cursor.fetchall()
ssd = pd.DataFrame(ssd)
sql = "SELECT * FROM capstone_modules.hdd;"
cursor.execute(sql)
hdd = cursor.fetchall()
hdd = pd.DataFrame(hdd)

form = cgi.FieldStorage()
usage = form["usage"].value
ramspace = form["ramspace"].value
ssdspace = form["ssdspace"].value
hddspace = form["hddspace"].value
budget = int(form["budget"].value)
"""
usage = 'office'
ssdspace = '128GB'
ramspace = '16'
hddspace = '1TB'
budget = 2000000
"""
def ram_set():
    rno, amount = 0, 1
    if ramspace == '8':
        rno = 0
        return rno, amount
    elif ramspace == '16':
        rno = 1
        return rno, amount
    elif ramspace == '32':
        rno = 4
        return rno, amount
    else:
        rno = 4
        amount = 2
        return rno, amount

def ssd_set():
    sno = 0
    if ssdspace == '128GB':
        sno = 16
        return sno
    elif ssdspace == '250GB':
        if mb.loc[m]['M2'] == 0:
            sno = 4
            return sno
        else:
            sno = 12
            return sno
    elif ssdspace == '500GB':
        if mb.loc[m]['M2'] == 0:
            sno = 5
            return sno
        else:
            sno = 13
            return sno
    elif ssdspace == '1TB':
        if mb.loc[m]['M2'] == 0:
            sno = 6
            return sno
        else:
            sno = 14
            return sno
    else:
        if mb.loc[m]['M2'] == 0:
            sno = 7
            return sno
        else:
            sno = 15
            return sno

def hdd_set():
    hno = 0
    if hddspace == '1TB':
        hno = 0
        return hno
    elif hddspace == '2TB':
        hno = 1
        return hno
    elif hddspace == '3TB':
        hno = 2
        return hno
    elif hddspace == '4TB':
        hno = 3
        return hno
    elif hddspace == '0':
        hno = 6
        return hno
    else:
        hno = 10
        return hno

def vga_up():
    global main_sum
    global v
    i = v + 1
    if v == 286:
        return 0
    elif vga.loc[i]['POWER'] <= psu.loc[p]['POWER']:
        if (main_sum - vga.loc[v]['PRICE'] + vga.loc[i]['PRICE']) <= main_price:
            main_sum = main_sum - vga.loc[v]['PRICE'] + vga.loc[i]['PRICE']
            v = i
            return 0
        else:
            return 2
    else:
        psu_up(i)
        return 0


def psu_up(a):
    global main_sum
    global v
    global p
    i = 0
    while (i < 182):
        if i == p:
            i += 1
        elif vga.loc[a]['POWER'] <= psu.loc[i]['POWER']:
            if (main_sum - vga.loc[v]['PRICE'] + vga.loc[a]['PRICE'] - psu.loc[p]['PRICE'] + psu.loc[i]['PRICE']) < main_price:
                main_sum = main_sum - vga.loc[v]['PRICE'] + vga.loc[a]['PRICE'] - psu.loc[p]['PRICE'] + psu.loc[i]['PRICE']
                p = i
                v = a
                return 0
            else:
                return 0
        else:
            i += 1


def cpu_up():
    global main_sum
    global c
    global m
    i = c + 1
    if c == 73:
        return 0
    elif cpu.loc[i]['SOCKET'] == mb.loc[m]['SOCKET']:
        if (main_sum - cpu.loc[c]['PRICE'] + cpu.loc[i]['PRICE']) < main_price:
            main_sum = main_sum - cpu.loc[c]['PRICE'] + cpu.loc[i]['PRICE']
            c = i
            return 0
        else:
            return 2
    else:
        mb_up(i)
        return 0

def cpu_uhd():
    global main_sum
    global c
    global m
    for i in range(c+1, 74):
        if len(cpu.loc[i]['IGP']) != 0:
            if cpu.loc[i]['SOCKET'] == mb.loc[m]['SOCKET']:
                if (main_sum - cpu.loc[c]['PRICE'] + cpu.loc[i]['PRICE']) < main_price:
                    main_sum = main_sum - cpu.loc[c]['PRICE'] + cpu.loc[i]['PRICE']
                    c = i
                    return 0
                else:
                    return 2
            else:
                mb_up(i)
                return 0
        elif i == 73:
            return 5
        else:
            i += 1

def mb_up(a):
    global main_sum
    global m
    global c
    i = 0
    while (i < 388):
        if i == m:
            i += 1
        elif cpu.loc[a]['SOCKET'] == mb.loc[i]['SOCKET']:
            if (main_sum - cpu.loc[c]['PRICE'] + cpu.loc[a]['PRICE'] - mb.loc[m]['PRICE'] + mb.loc[i]['PRICE']) < main_price:
                main_sum = main_sum - cpu.loc[c]['PRICE'] + cpu.loc[a]['PRICE'] - mb.loc[m]['PRICE'] + mb.loc[i]['PRICE']
                c = a
                m = i
                return 1
            else:
                return 0
        else:
            i += 1


#case_up 이전에 사용할것
def cpucooler_up():
    global sub_sum
    global cc
    global c
    if cpu.loc[c]['SOCKET'] == 'AM4':
        for i in range(cc, 147):
            if cpucooler.loc[i]['SOCKET4'] == 'AM4':
                if (sub_sum - cpucooler.loc[cc]['PRICE'] + cpucooler.loc[i]['PRICE']) < sub_price:
                    if cpucooler.loc[i]['PRICE'] < (sub_price / 2):
                        sub_sum = sub_sum - cpucooler.loc[cc]['PRICE'] + cpucooler.loc[i]['PRICE']
                        cc = i
    if cpu.loc[c]['SOCKET'] == 'TR4':
        for i in range(cc, 147):
            if cpucooler.loc[i]['SOCKET3'] == 'TR4':
                if (sub_sum - cpucooler.loc[cc]['PRICE'] + cpucooler.loc[i]['PRICE']) < sub_price:
                    if (sub_sum - cpucooler.loc[cc]['PRICE'] + cpucooler.loc[i]['PRICE']) < sub_price:
                        sub_sum = sub_sum - cpucooler.loc[cc]['PRICE'] + cpucooler.loc[i]['PRICE']
                        cc = i
    if cpu.loc[c]['SOCKET'] == '1151v2':
        for i in range(cc, 147):
            if cpucooler.loc[i]['SOCKET2'] == 'LGA115x':
                if (sub_sum - cpucooler.loc[cc]['PRICE'] + cpucooler.loc[i]['PRICE']) < sub_price:
                    if (sub_sum - cpucooler.loc[cc]['PRICE'] + cpucooler.loc[i]['PRICE']) < sub_price:
                        sub_sum = sub_sum - cpucooler.loc[cc]['PRICE'] + cpucooler.loc[i]['PRICE']
                        cc = i
    if cpu.loc[c]['SOCKET'] == '2066':
        for i in range(cc, 147):
            if cpucooler.loc[i]['SOCKET1'] == 'LGA2066':
                if (sub_sum - cpucooler.loc[cc]['PRICE'] + cpucooler.loc[i]['PRICE']) < sub_price:
                    if (sub_sum - cpucooler.loc[cc]['PRICE'] + cpucooler.loc[i]['PRICE']) < sub_price:
                        sub_sum = sub_sum - cpucooler.loc[cc]['PRICE'] + cpucooler.loc[i]['PRICE']
                        cc = i


def case_up():
    global sub_sum
    global cs
    global m
    global p
    if mb.loc[m]['SIZE'] == 'ATX':
        for i in range(cs, 255):
            if case.loc[i]['SIZE'] == 'ATX':
                if vga.loc[v]['SIZE'] < case.loc[i]['VGASIZE']:
                    if cpucooler.loc[cc]['HEIGHT'] < case.loc[i]['CPUSIZE']:
                        if (sub_sum - case.loc[cs]['PRICE'] + case.loc[i]['PRICE']) < sub_price:
                            sub_sum = sub_sum - case.loc[cs]['PRICE'] + case.loc[i]['PRICE']
                            cs = i
    if mb.loc[m]['SIZE'] == 'M-ATX':
        for i in range(cs, 255):
            if case.loc[i]['SIZE'] == 'M-ATX' or 'ATX':
                if psu.loc[p]['SIZE'] == case.loc[i]['SIZE']:
                    if vga.loc[v]['SIZE'] < case.loc[i]['VGASIZE']:
                        if cpucooler.loc[cc]['HEIGHT'] < case.loc[i]['CPUSIZE']:
                            if (sub_sum - case.loc[cs]['PRICE'] + case.loc[i]['PRICE']) < sub_price:
                                sub_sum = sub_sum - case.loc[cs]['PRICE'] + case.loc[i]['PRICE']
                                cs = i


global c0, m0, v0, p0, cs0, cc0, r0, ramount0, h0, s0
global c1, m1, v1, p1, cs1, cc1, r1, ramount1, h1, s1

if usage == 'game':
    c, m, v, p, cs, cc, r, ramount, h, s = 5, 9, 15, 6, 0, 0, 0, 1, 0, 0
    r, ramount = ram_set()
    main_sum = cpu.loc[c]['PRICE'] + mb.loc[m]['PRICE'] + psu.loc[p]['PRICE'] + ram.loc[r]['PRICE'] * ramount + \
               vga.loc[v]['PRICE'] + hdd.loc[h]['PRICE'] + ssd.loc[s]['PRICE']
    sub_sum = case.loc[cs]['PRICE'] + cpucooler.loc[cc]['PRICE']
    max_price = budget
    main_price = max_price * 0.9
    sub_price = max_price * 0.1
    count = 0
    while True:
        if (main_sum + sub_sum > max_price):
            break
        if (count < 20):
            limit1 = vga_up()
            if limit1 == 2:
                break
            count += 1
        if (count >= 20):
            limit2 = cpu_up()
            if limit2 == 2:
                break
            count = 0
    s = ssd_set()
    h = hdd_set()
    cpucooler_up()
    case_up()
    max_sum0 = main_sum + sub_sum
    c0, m0, v0, p0, cs0, cc0, r0, ramount0, h0, s0 = c, m, v, p, cs, cc, r, ramount, h, s

    c, m, v, p, cs, cc, r, ramount, h, s = 5, 9, 15, 6, 0, 0, 0, 1, 0, 0
    r, ramount = ram_set()
    count = 0
    while True:
        if (main_sum + sub_sum > max_price):
            break
        if (count < 18):
            limit1 = vga_up()
            if limit1 == 2:
                break
            count += 1
        if (count >= 18):
            limit2 = cpu_up()
            if limit2 == 2:
                break
            count = 0
    s = ssd_set()
    h = hdd_set()
    cpucooler_up()
    case_up()
    max_sum1 = main_sum + sub_sum
    c1, m1, v1, p1, cs1, cc1, r1, ramount1, h1, s1 = c, m, v, p, cs, cc, r, ramount, h, s

    c, m, v, p, cs, cc, r, ramount, h, s = 5, 9, 15, 6, 0, 0, 0, 1, 0, 0
    r, ramount = ram_set()
    count = 0
    while True:
        if (main_sum + sub_sum > max_price):
            break
        if (count < 15):
            limit1 = vga_up()
            if limit1 == 2:
                break
            count += 1
        if (count >= 15):
            limit2 = cpu_up()
            if limit2 == 2:
                break
            count = 0
    s = ssd_set()
    h = hdd_set()
    cpucooler_up()
    case_up()
    max_sum = main_sum + sub_sum

if usage == 'office':
    c, m, p, cs, cc, r, ramount, h, s, v= 0, 14, 6, 0, 0, 0, 2, 0, 0, 287
    r, ramount = ram_set()
    h = hdd_set()
    if h == 10:
        main_sum = cpu.loc[c]['PRICE'] + mb.loc[m]['PRICE'] + psu.loc[p]['PRICE'] + ram.loc[r]['PRICE'] * ramount \
                   + ssd.loc[s]['PRICE']
    else:
        main_sum = cpu.loc[c]['PRICE'] + mb.loc[m]['PRICE'] + psu.loc[p]['PRICE'] + ram.loc[r]['PRICE'] * ramount \
                   + ssd.loc[s]['PRICE'] + hdd.loc[h]['PRICE']
    sub_sum = case.loc[cs]['PRICE'] + cpucooler.loc[cc]['PRICE']
    max_price = budget
    main_price = max_price * 0.9
    sub_price = max_price * 0.1

    while True:
        if (main_sum + sub_sum > max_price):
            break
        limit2 = cpu_uhd()
        if limit2 != 0:
            break
    s = ssd_set()
    cpucooler_up()
    case_up()
    c0, m0, p0, cs0, cc0, r0, ramount0, h0, s0, v0 = c, m, p, cs, cc, r, ramount, h, s, v
    max_sum0 = main_sum + sub_sum

    main_price = max_price * 0.92
    sub_price = max_price * 0.08

    c, m, p, cs, cc, r, ramount, h, s, v = 0, 14, 6, 0, 0, 0, 2, 0, 0, 287
    r, ramount = ram_set()
    h = hdd_set()
    while True:
        if (main_sum + sub_sum > max_price):
            break
        limit2 = cpu_uhd()
        if limit2 != 0:
            break
    s = ssd_set()
    cpucooler_up()
    case_up()
    c1, m1, p1, cs1, cc1, r1, ramount1, h1, s1, v1 = c, m, p, cs, cc, r, ramount, h, s, v
    max_sum1 = main_sum + sub_sum

    main_price = max_price * 0.94
    sub_price = max_price * 0.06

    c, m, p, cs, cc, r, ramount, h, s, v = 0, 14, 6, 0, 0, 0, 2, 0, 0, 287
    r, ramount = ram_set()
    h = hdd_set()
    while True:
        if (main_sum + sub_sum > max_price):
            break
        limit2 = cpu_uhd()
        if limit2 != 0:
            break
    s = ssd_set()
    cpucooler_up()
    case_up()
    max_sum = main_sum + sub_sum



if usage == 'TASK':
    c, m, v, p, cs, cc, r, ramount, h, s = 13, 9, 15, 6, 0, 0, 0, 2, 0, 0
    r, ramount = ram_set()
    h = hdd_set()
    if h == 10:
        main_sum = cpu.loc[c]['PRICE'] + mb.loc[m]['PRICE'] + psu.loc[p]['PRICE'] + ram.loc[r]['PRICE'] * ramount \
                   + ssd.loc[s]['PRICE'] + vga.loc[v]['PRICE']
    else:
        main_sum = cpu.loc[c]['PRICE'] + mb.loc[m]['PRICE'] + psu.loc[p]['PRICE'] + ram.loc[r]['PRICE'] * ramount \
                   + ssd.loc[s]['PRICE'] + vga.loc[v]['PRICE'] + hdd.loc[h]['PRICE']
    sub_sum = case.loc[cs]['PRICE'] + cpucooler.loc[cc]['PRICE']
    max_price = budget
    main_price = max_price * 0.9
    sub_price = max_price * 0.1

    count = 0
    while True:
        if (main_sum + sub_sum > max_price):
            break
        if (count < 5):
            limit1 = vga_up()
            if limit1 == 2:
                break
            count += 1
        if (count >= 5):
            limit2 = cpu_up()
            if limit2 == 2:
                break
            count = 0
    s = ssd_set()
    cpucooler_up()
    case_up()
    c0, m0, v0, p0, cs0, cc0, r0, ramount0, h0, s0 = c, m, v, p, cs, cc, r, ramount, h, s
    max_sum0 = main_sum + sub_sum

    c, m, v, p, cs, cc, r, ramount, h, s = 13, 9, 15, 6, 0, 0, 0, 2, 0, 0
    r, ramount = ram_set()
    h = hdd_set()
    count = 0
    while True:
        if (main_sum + sub_sum > max_price):
            break
        if (count < 6):
            limit1 = vga_up()
            if limit1 == 2:
                break
            count += 1
        if (count >= 6):
            limit2 = cpu_up()
            if limit2 == 2:
                break
            count = 0
    s = ssd_set()
    cpucooler_up()
    case_up()
    c1, m1, v1, p1, cs1, cc1, r1, ramount1, h1, s1 = c, m, v, p, cs, cc, r, ramount, h, s
    max_sum1 = main_sum + sub_sum

    c, m, v, p, cs, cc, r, ramount, h, s = 13, 9, 15, 6, 0, 0, 0, 2, 0, 0
    r, ramount = ram_set()
    h = hdd_set()
    count = 0
    while True:
        if (main_sum + sub_sum > max_price):
            break
        if (count < 8):
            limit1 = vga_up()
            if limit1 == 2:
                break
            count += 1
        if (count >= 8):
            limit2 = cpu_up()
            if limit2 == 2:
                break
            count = 0
    s = ssd_set()
    cpucooler_up()
    case_up()
    max_sum = main_sum + sub_sum
"""
print('PRICE // CPU: %d, MB: %d, VGA: %d, PSU: %d' % (cpu.loc[c]['PRICE'], mb.loc[m]['PRICE'], vga.loc[v]['PRICE'], psu.loc[p]['PRICE']))
print('INDEX // CPU: %d, MB: %d, VGA: %d, PSU: %d\n' % (c, m, v, p))
# print('PRICE // RAM: %d, SSD: %d, HDD: %d'%(ram.loc[r]['PRICE'] * 2, ssd.loc[s]['PRICE'], hdd.loc[h]['PRICE']))
# print('INDEX // RAM: %d, SSD: %d, HDD: %d\n'%(r, s, h))
print('PRICE // RAM: %d, SSD: %d' % (ram.loc[r]['PRICE'] * ramount, ssd.loc[s]['PRICE']))
print('INDEX // RAM: %d, SSD: %d\n' % (r, s))
print('PRICE // CASE: %d, CPUCOOLER: %d' % (case.loc[cs]['PRICE'], cpucooler.loc[cc]['PRICE']))
print('INDEX // CASE: %d, CPUCOOLER: %d\n' % (cs, cc))
print('Total price is', main_sum + sub_sum, '\\')
"""


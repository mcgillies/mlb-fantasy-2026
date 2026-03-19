#!/usr/bin/env python3
"""Parse ESPN rankings from copy-pasted draft room text."""

import re
import csv

raw_text = """1

Shohei Ohtani
LAD
DH/SP
DH1
$101
$78
2

Aaron Judge
NYY
OF/DH
OF1
$79
$63
3

Juan Soto
NYM
OF
OF2
$77
$61
4

Paul Skenes
PIT
SP
SP2
$72
$58
5

Bobby Witt Jr.
KC
SS
SS1
$68
$55
6

Tarik Skubal
DET
SP
SP3
$67
$54
7

Jose Ramirez
CLE
3B/DH
3B1
$57
$48
8

Garrett Crochet
BOS
SP
SP4
$48
$41
9

Kyle Tucker
LAD
OF
OF3
$46
$40
10

Ronald Acuna Jr.
ATL
OF
OF4
$45
$39
11

Ketel Marte
ARI
2B/DH
2B1
$43
$38
12

Cristopher Sanchez
PHI
SP
SP5
$40
$36
13

Cal Raleigh
SEA
C/DH
C1
$39
$35
14

Fernando Tatis Jr.
SD
OF
OF5
$39
$35
15

Logan Gilbert
SEA
SP
SP6
$38
$34
16

Junior Caminero
TB
3B
3B2
$36
$33
17

Corbin Carroll
ARI
OF
OF6
$36
$33
18

Gunnar Henderson
BAL
SS
SS2
$36
$33
19

Yoshinobu Yamamoto
LAD
SP
SP7
$35
$33
20

Bryan Woo
SEA
SP
SP8
$35
$32
21

Kyle Schwarber
PHI
DH
DH2
$34
$32
22

Logan Webb
SF
SP
SP9
$33
$31
23

Manny Machado
SD
3B
3B3
$33
$31
24

Hunter Brown
HOU
SP
SP10
$32
$31
25

Julio Rodriguez
SEA
OF
OF7
$32
$30
26

Vladimir Guerrero Jr.
TOR
1B/DH
1B1
$31
$30
27

William Contreras
MIL
C/DH
C2
$30
$29
28

Max Fried
NYY
SP
SP11
$30
$29
29

Chris Sale
ATL
SP
SP12
$29
$29
30

Joe Ryan
MIN
SP
SP13
$29
$28
31

Alex Bregman
CHC
3B
3B4
$28
$28
32

Yordan Alvarez
HOU
OF/DH
OF8
$28
$27
33

Jesus Luzardo
PHI
SP
SP14
$27
$27
34

Jacob deGrom
TEX
SP
SP15
$27
$27
35

Jackson Chourio
MIL
OF
OF9
$26
$27
36

Mookie Betts
LAD
SS
SS3
$26
$26
37

Mason Miller
SD
RP
RP1
$25
$25
38

George Kirby
SEA
SP
SP16
$24
$25
39

Brent Rooker
ATH
OF/DH
OF10
$24
$25
40

Nico Hoerner
CHC
2B
2B2
$24
$25
41

Freddy Peralta
NYM
SP
SP17
$23
$24
42

Francisco Lindor
NYM
SS
SS4
$22
$24
43

Cade Smith
CLE
RP
RP2
$22
$23
44

Cody Bellinger
NYY
OF
OF11
$21
$23
45

Cole Ragans
KC
SP
SP18
$21
$23
46

Framber Valdez
DET
SP
SP19
$21
$22
47

Steven Kwan
CLE
OF
OF12
$20
$22
48

Dylan Cease
TOR
SP
SP20
$19
$22
49

Edwin Diaz
LAD
RP
RP3
$19
$21
50
UP
Roman Anthony
BOS
OF
OF13
$19
$21
51

Kevin Gausman
TOR
SP
SP21
$18
$21
52

Elly De La Cruz
CIN
SS
SS5
$18
$21
53

Andres Munoz
SEA
RP
RP4
$18
$20
54

Jarren Duran
BOS
OF
OF14
$17
$20
55

Jose Altuve
HOU
2B/OF/DH
2B3
$17
$20
56

Nick Pivetta
SD
SP
SP22
$16
$19
57

Ben Rice
NYY
1B/C/DH
1B14
$16
$19
58

Maikel Garcia
KC
3B
3B5
$15
$18
59

George Springer
TOR
OF/DH
OF15
$15
$18
60

Jhoan Duran
PHI
RP
RP5
$15
$18
61

Geraldo Perdomo
ARI
SS
SS6
$14
$18
62

Jazz Chisholm Jr.
NYY
2B/3B
2B4
$14
$17
63

Sonny Gray
BOS
SP
SP23
$14
$17
64

Jackson Merrill
SD
OF
OF16
$13
$17
65

Matt Olson
ATL
1B
1B2
$13
$17
66

Zack Wheeler
PHI
SP
SP24
$13
$17
67

Brice Turang
MIL
2B
2B5
$13
$17
68

Christian Yelich
MIL
DH
DH3
$13
$17
69

Devin Williams
NYM
RP
RP6
$13
$16
70

Ryan Pepiot
TB
SP
SP25
$13
$16
71

Pete Crow-Armstrong
CHC
OF
OF18
$12
$16
72

Nathan Eovaldi
TEX
SP
SP26
$12
$16
73

Shea Langeliers
ATH
C
C4
$12
$16
74

Ozzie Albies
ATL
2B
2B6
$11
$15
75

Eury Perez
MIA
SP
SP27
$11
$15
76

Pete Alonso
BAL
1B
1B3
$11
$15
77

Ian Happ
CHC
OF
OF19
$10
$15
78

Luis Castillo
SEA
SP
SP28
$10
$15
79

Nick Kurtz
ATH
1B
1B4
$10
$14
80

Trea Turner
PHI
SS
SS7
$10
$14
81

David Bednar
NYY
RP
RP7
$10
$14
82

Kyle Bradish
BAL
SP
SP29
$10
$14
83

Taylor Ward
BAL
OF
OF20
$9
$14
84

Will Smith
LAD
C
C5
$9
$14
85
UP
Vinnie Pasquantino
KC
1B/DH
1B5
$9
$14
86
DOWN
Blake Snell
LAD
SP
SP30
$9
$13
87

Seiya Suzuki
CHC
OF/DH
OF21
$9
$13
88

Aroldis Chapman
BOS
RP
RP8
$9
$13
89

James Wood
WSH
OF/DH
OF22
$9
$13
90

Brandon Woodruff
MIL
SP
SP31
$8
$13
91

Drake Baldwin
ATL
C
C6
$8
$13
92

Josh Naylor
SEA
1B/DH
1B6
$8
$13
93

Gleyber Torres
DET
2B
2B7
$8
$12
94

Randy Arozarena
SEA
OF
OF23
$8
$12
95

Adley Rutschman
BAL
C
C7
$8
$12
96
DOWN
Spencer Strider
ATL
SP
SP32
$7
$12
97

Austin Riley
ATL
3B
3B7
$7
$12
98

Tanner Bibee
CLE
SP
SP33
$7
$12
99

Wyatt Langford
TEX
OF
OF24
$7
$11
100

Salvador Perez
KC
C/1B/DH
C8
$7
$11
101

Freddie Freeman
LAD
1B
1B7
$6
$11
102

Corey Seager
TEX
SS
SS8
$6
$11
103

Raisel Iglesias
ATL
RP
RP9
$6
$11
104

Brandon Nimmo
TEX
OF
OF25
$6
$11
105

Zac Gallen
ARI
SP
SP34
$6
$11
106

Yainer Diaz
HOU
C/DH
C9
$6
$11
107
UP
Nolan McLean
NYM
SP
SP35
$6
$10
108

Alec Burleson
STL
OF/1B/DH
OF26
$5
$10
109

Eugenio Suarez
CIN
3B
3B8
$5
$10
110

Luke Keaschall
MIN
2B
2B8
$5
$10
111
DOWN
Rafael Devers
SF
1B/DH
1B8
$5
$10
112

Jacob Misiorowski
MIL
SP
SP36
$5
$10
113

Riley Greene
DET
OF/DH
OF27
$5
$10
114

Emilio Pagan
CIN
RP
RP10
$5
$9
115

Bo Bichette
NYM
SS
SS9
$5
$9
116
DOWN
Chase Burns
CIN
SP
SP37
$4
$9
117

Bryce Harper
PHI
1B
1B9
$4
$9
118

Matt Chapman
SF
3B
3B9
$4
$9
119

Tyler Soderstrom
ATH
OF/1B
OF28
$4
$9
120

Nick Lodolo
CIN
SP
SP38
$4
$9
121

Agustin Ramirez
MIA
C/DH
C10
$4
$9
122

Michael King
SD
SP
SP39
$4
$8
123

Yandy Diaz
TB
1B/DH
1B10
$4
$8
124
UP
Brendan Donovan
SEA
2B
2B9
$4
$8
125

Bryan Reynolds
PIT
OF/DH
OF29
$3
$8
126
UP
Drew Rasmussen
TB
SP
SP40
$3
$8
127

Caleb Durbin
BOS
3B
3B10
$3
$8
128

Emmet Sheehan
LAD
SP
SP41
$3
$7
129

Ranger Suarez
BOS
SP
SP42
$3
$7
130

Willy Adames
SF
SS
SS10
$3
$7
131

Tyler Glasnow
LAD
SP
SP43
$3
$7
132

Byron Buxton
MIN
OF
OF30
$3
$7
133

Marcus Semien
NYM
2B
2B10
$3
$7
134

Andrew Abbott
CIN
SP
SP44
$3
$7
135

MacKenzie Gore
TEX
SP
SP45
$2
$7
136

Michael Harris II
ATL
OF
OF31
$2
$7
137
DOWN
Andy Pages
LAD
OF
OF35
$2
$7
138

Jeremy Pena
HOU
SS
SS11
$2
$7
139

Oneil Cruz
PIT
OF
OF34
$2
$7
140

Hunter Goodman
COL
C/DH
C11
$2
$7
141

Alejandro Kirk
TOR
C
C12
$2
$6
142

Jakob Marsee
MIA
OF
OF32
$2
$6
143
UP
Daylen Lile
WSH
OF
OF33
$2
$6
144
UP
Bryan Abreu
HOU
RP
RP11
$2
$6
145

Gavin Williams
CLE
SP
SP46
$2
$6
146

Jacob Wilson
ATH
SS
SS12
$2
$6
147

Cam Schlittler
NYY
SP
SP47
$2
$6
148

Jung Hoo Lee
SF
OF
OF36
$2
$6
149
UP
Griffin Jax
TB
RP
RP12
$2
$6
150

Matthew Boyd
CHC
SP
SP48
$2
$6
151

CJ Abrams
WSH
SS
SS13
$1
$6
152

Robbie Ray
SF
SP
SP49
$1
$6
153

Shota Imanaga
CHC
SP
SP50
$1
$5
154

Kyle Stowers
MIA
OF
OF37
$1
$5
155
DOWN
Josh Hader
HOU
RP
RP13
$1
$5
156

Luis Arraez
SF
1B/DH
1B12
$1
$5
157
UP
Abner Uribe
MIL
RP
RP14
$1
$5
158

Gabriel Moreno
ARI
C
C13
$1
$5
159

Sal Frelick
MIL
OF
OF38
$1
$5
160

Zach Neto
LAA
SS
SS14
$1
$5
161
DOWN
Bryson Stott
PHI
2B
2B11
$1
$5
162

Jeff Hoffman
TOR
RP
RP15
$1
$5
163

Teoscar Hernandez
LAD
OF
OF39
$1
$5
164

Jack Flaherty
DET
SP
SP51
$1
$5
165

Xavier Edwards
MIA
2B/SS
2B12
$1
$5
166

Otto Lopez
MIA
SS/2B
SS17
$1
$5
167

Pete Fairbanks
MIA
RP
RP16
$1
$4
168

Merrill Kelly
ARI
SP
SP52
$1
$4
169

Trevor Rogers
BAL
SP
SP53
$1
$4
170

Brandon Lowe
PIT
2B
2B14
$1
$4
171

TJ Friedl
CIN
OF
OF40
$1
$4
172

Sandy Alcantara
MIA
SP
SP54
$1
$4
173
UP
Michael Busch
CHC
1B
1B13
$1
$4
174
DOWN
Ryan Helsley
BAL
RP
RP17
$1
$4
175

Shane Baz
BAL
SP
SP55
$1
$4
176

Ernie Clement
TOR
3B/2B/SS
3B13
$1
$4
177
UP
Jac Caglianone
KC
OF
OF41
$1
$4
178

Tatsuya Imai
HOU
SP
SP56
$1
$4
179

Kenley Jansen
DET
RP
RP18
$1
$4
180

Dansby Swanson
CHC
SS
SS15
$1
$4
181

Aaron Nola
PHI
SP
SP57
$1
$4
182

Yusei Kikuchi
LAA
SP
SP58
$1
$3
183
UP
Kazuma Okamoto
TOR
3B
3B11
$1
$3
184

Kris Bubic
KC
SP
SP59
$1
$3
185
UP
Ryan O'Hearn
PIT
1B/OF/DH
1B22
$1
$3
186
DOWN
Trevor Megill
MIL
RP
RP19
$1
$3
187

Jose Soriano
LAA
SP
SP60
$1
$3
188
UP
Heliot Ramos
SF
OF
OF43
$1
$3
189

Bubba Chandler
PIT
SP
SP61
$1
$3
190

J.T. Realmuto
PHI
C
C14
$1
$3
191

Jo Adell
LAA
OF
OF44
$0
$3
192
DOWN
Luis Garcia Jr.
WSH
2B
2B16
$0
$3
193

Bailey Ober
MIN
SP
SP62
$0
$3
194

Isaac Paredes
HOU
3B
3B12
$0
$3
195

Christian Walker
HOU
1B
1B16
$0
$3
196

Ceddanne Rafaela
BOS
OF/2B
OF45
$0
$3
197

J.P. Crawford
SEA
SS
SS16
$0
$3
198

Jeff McNeil
ATH
2B/OF
2B22
$0
$2
199

Joe Musgrove
SD
SP
SP63
$0
$2
200

Wilyer Abreu
BOS
OF
OF47
$0
$2
201

Marcell Ozuna
PIT
DH
DH4
$0
$2
202

Daulton Varsho
TOR
OF
OF48
$0
$2
203

Daniel Palencia
CHC
RP
RP20
$0
$2
204

Mitch Keller
PIT
SP
SP64
$0
$2
205

Lawrence Butler
ATH
OF
OF49
$0
$2
206

Spencer Torkelson
DET
1B
1B17
$0
$2
207

Adolis Garcia
PHI
OF
OF50
$0
$2
208
UP
Gerrit Cole
NYY
SP
SP65
$0
$2
209

Alec Bohm
PHI
3B
3B14
$0
$2
210

Edward Cabrera
CHC
SP
SP66
$0
$2
211

Samuel Basallo
BAL
C
C15
$0
$2
212

Jorge Polanco
NYM
2B/DH
2B17
$0
$2
213

Xander Bogaerts
SD
SS
SS19
$0
$2
214

Brady Singer
CIN
SP
SP67
$0
$2
215

Kerry Carpenter
DET
OF/DH
OF51
$0
$2
216
DOWN
Carlos Rodon
NYY
SP
SP68
$0
$2
217

Nolan Arenado
ARI
3B
3B15
$0
$1
218

Noelvi Marte
CIN
OF/3B
OF52
$0
$1
219

Michael Wacha
KC
SP
SP69
$0
$1
220

Matt McLain
CIN
2B
2B18
$0
$1
221

Cade Horton
CHC
SP
SP70
$0
$1
222

Seth Lugo
KC
SP
SP71
$0
$1
223

Austin Wells
NYY
C
C16
$0
$1
224

Mike Trout
LAA
OF/DH
OF53
$0
$1
225

Jake Cronenworth
SD
2B
2B19
$0
$1
226

Kyle Teel
CWS
C
C17
$0
$1
227

Chandler Simpson
TB
OF
OF54
$0
$1
228
DOWN
Trey Yesavage
TOR
SP
SP72
$0
$1
229
UP
Miguel Vargas
CWS
3B/1B
3B16
$0
$1
230

Jonathan India
KC
2B/3B/OF/DH
2B23
$0
$1
231

Shane McClanahan
TB
SP
SP73
$0
$1
232

Andrew Benintendi
CWS
OF/DH
OF56
$0
$1
233

Clay Holmes
NYM
SP
SP74
$0
$1
234

Willson Contreras
BOS
1B
1B19
$0
$1
235
DOWN
Jackson Holliday
BAL
2B
2B21
$0
$1
236

Ryan Jeffers
MIN
C/DH
C18
$0
$1
237

Ramon Laureano
SD
OF
OF57
$0
$1
238

Shane Smith
CWS
SP
SP75
$0
$1
239

Noah Cameron
KC
SP
SP76
$0
$1
240
DOWN
Carlos Estevez
KC
RP
RP21
$0
$1
241

Jack Leiter
TEX
SP
SP77
$0
$1
242

Cody Ponce
TOR
SP
SP78
$0
$1
243

Lars Nootbaar
STL
OF
OF58
$0
$1
244

Chris Bassitt
BAL
SP
SP79
$0
$1
245

Carlos Correa
HOU
SS/3B
SS21
$0
$1
246

Dylan Crews
WSH
OF
OF59
$0
$1
247

Ian Seymour
TB
RP/SP
RP
$0
$1
248
UP
Carter Jensen
KC
C/DH
C19
$0
$1
249
DOWN
Trent Grisham
NYY
OF
OF60
$0
$1
250

Ivan Herrera
STL
DH
DH5
$0
$1
251

Ryan Walker
SF
RP
RP22
$0
$1
252

Kodai Senga
NYM
SP
SP81
$0
$1
253

Nolan Schanuel
LAA
1B
1B20
$0
$1
254

Luis Robert Jr.
NYM
OF
OF61
$0
$1
255

Trevor Larnach
MIN
OF/DH
OF62
$0
$1
256

Spencer Steer
CIN
1B
1B21
$0
$1
257

David Peterson
NYM
SP
SP82
$0
$1
258

Gavin Sheets
SD
OF/DH
OF63
$0
$1
259
UP
Robert Garcia
TEX
RP
RP23
$0
$1
260

Addison Barger
TOR
3B/OF
3B25
$0
$1
261

Brayan Bello
BOS
SP
SP83
$0
$1
262

Francisco Alvarez
NYM
C
C20
$0
$1
263

Trevor Story
BOS
SS
SS22
$0
$1
264

Jasson Dominguez
NYY
OF
OF65
$0
$1
265
DOWN
Shane Bieber
TOR
SP
SP84
$0
$1
266

Robert Suarez
ATL
RP
RP24
$0
$1
267
UP
Andrew Vaughn
MIL
1B
1B23
$0
$1
268

Max Muncy
LAD
3B
3B18
$0
$1
269

Harrison Bader
SF
OF
OF66
$0
$1
270

Dillon Dingler
DET
C
C21
$0
$1
271

Chad Patrick
MIL
SP
SP85
$0
$1
272

Andres Gimenez
TOR
2B
2B24
$0
$1
273

Giancarlo Stanton
NYY
OF/DH
OF67
$0
$1
274

Jeffrey Springs
ATH
SP
SP86
$0
$1
275

Jonathan Aranda
TB
1B
1B24
$0
$1
276

Cedric Mullins
TB
OF
OF68
$0
$1
277

Reid Detmers
LAA
RP
RP25
$0
$0
278

Masyn Winn
STL
SS
SS23
$0
$0
279

Joey Cantillo
CLE
RP/SP
RP
$0
$0
280

Tyler Stephenson
CIN
C
C22
$0
$0
281

Jameson Taillon
CHC
SP
SP88
$0
$0
282
UP
Chase Meidroth
CWS
SS/2B
SS25
$0
$0
283

Sal Stewart
CIN
1B/3B
1B26
$0
$0
284

Chase DeLauter
CLE
OF
OF69
$0
$0
285

Carson Kelly
CHC
C
C23
$0
$0
286

Brandon Pfaadt
ARI
SP
SP89
$0
$0
287

Jeremiah Estrada
SD
RP
RP26
$0
$0
288

Bo Naylor
CLE
C
C24
$0
$0
289

Brenton Doyle
COL
OF
OF70
$0
$0
290
DOWN
Royce Lewis
MIN
3B
3B21
$0
$0
291

Brooks Lee
MIN
SS/2B/3B
SS27
$0
$0
292

Grayson Rodriguez
LAA
SP
SP90
$0
$0
293

Ezequiel Tovar
COL
SS
SS24
$0
$0
294

Dominic Canzone
SEA
OF
OF71
$0
$0
295

Keibert Ruiz
WSH
C
C25
$0
$0
296

Ryne Nelson
ARI
SP/RP
SP91
$0
$0
297

Evan Carter
TEX
OF
OF72
$0
$0
298
DOWN
Sean Manaea
NYM
SP
SP92
$0
$0
299
UP
Mike Burrows
HOU
SP
SP93
$0
$0
300

Brandon Marsh
PHI
OF
OF73
$0
$0"""

def parse_rankings(text):
    """Parse the pasted ESPN rankings text into structured data."""
    lines = text.strip().split('\n')
    players = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Check if this line starts with a rank number
        rank_match = re.match(r'^(\d+)$', line)
        if rank_match:
            rank = int(rank_match.group(1))

            # Skip whitespace/UP/DOWN lines to find player name
            i += 1
            while i < len(lines) and (lines[i].strip() == '' or lines[i].strip() in ['UP', 'DOWN'] or 'UP' in lines[i] or 'DOWN' in lines[i]):
                i += 1

            if i >= len(lines):
                break

            name = lines[i].strip()
            i += 1

            if i >= len(lines):
                break
            team = lines[i].strip()
            i += 1

            if i >= len(lines):
                break
            position = lines[i].strip()
            i += 1

            # Skip position rank and dollar values
            while i < len(lines) and not re.match(r'^\d+$', lines[i].strip()):
                i += 1

            players.append({
                'ESPN_Rank': rank,
                'Name': name,
                'Team': team,
                'Position': position
            })
        else:
            i += 1

    return players

def write_csv(players, output_path):
    """Write players to CSV."""
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['ESPN_Rank', 'Name', 'Team', 'Position'])
        writer.writeheader()
        writer.writerows(players)

if __name__ == '__main__':
    players = parse_rankings(raw_text)
    output_path = '/Users/matthewgillies/mlb-fantasy-2026/data/espn/espn_rankings_2026.csv'
    write_csv(players, output_path)
    print(f"Wrote {len(players)} players to {output_path}")

    # Print first 10 for verification
    print("\nFirst 10 players:")
    for p in players[:10]:
        print(f"  {p['ESPN_Rank']}: {p['Name']} ({p['Team']}) - {p['Position']}")

    print("\nLast 5 players:")
    for p in players[-5:]:
        print(f"  {p['ESPN_Rank']}: {p['Name']} ({p['Team']}) - {p['Position']}")

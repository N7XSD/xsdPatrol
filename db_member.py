"""
Access MemberDB.  After data is moved to PatrolDB, MemberDB will be abandoned
"""

import datetime
from html.parser import HTMLParser
import logging
import re

import common

DATE_FORMAT_MSACCESS = "#%m/%d/%Y#"
MAXINT_MSACCESS = 2147483647
MININT_MSACCESS = -2147483648


member_dict = {
    1: 'BARBARADOR',    # Barbara Dorway
    2: 'BILLHEN',       # Bill Edwin Henriod
    3: 'BUDP',          # Bud Puckett
    4: 'CONNIED',       # Connie Daugherty
    5: 'DANIELLEL',     # Danielle Luthy
    6: 'DAVIDDOR',      # David Dorway
    7: 'DAVIDS',        # David Steinman
    8: 'ELLENB',        # Ellen Bachman
    13: 'BRIAND',        # Brian Dodd
    16: 'JENNIED',       # Jennie Dodd
    17: 'JUDYH',         # Judy Hunt
    21: 'JIMDUN',        # Jim Dunbar
    22: 'NANCYDUN',      # Nancy Dunbar
    24: 'JIMGAUG',       # Jim Gaughan
    25: 'ANNEG',         # Anne Green
    26: 'ERNIEM',        # Ernie Montgomery
    27: 'JANETMOS',      # Janet Moseley
    28: 'NANCYPOP',      # Nancy Popek
    29: 'MARYJOR',       # Mary Jo Richards
    30: 'SUESTEV',       # Sue Stevens
    31: 'WALTL',         # Walter LaMay (duplicate of 137)
    33: 'CAROLA',        # Carol Aker
    34: 'DICKA',         # Dick Aker
    35: 'TOMA',          # Tom Amenta
    36: 'HERBA',         # Herb Apfel
    37: 'BURTA',         # Burt Arnold
    38: 'JANEASHE',      # Jane Ashe
    39: 'RONA',          # Ron Atchison
    40: 'RICHARDA',      # Richard Augulis
    42: 'STANB',         # Stan Bachman
    43: 'LARRYB',        # Larry Bacon
    44: 'JAMESB',        # James Barr
    45: 'ROGERB',        # Roger Barrett
    46: 'LARRYBAU',      # Larry Baudler
    47: 'HELENBEAL',     # Helen Beal
    48: 'DANB',          # Dan Beer
    49: 'PATB',          # Pat Bemis
    50: 'MARYBIRD',      # Mary Bird
    51: 'SUSANB',        # Susan Blaisdell
    52: 'JERRYB',        # Jerry Borowski
    53: 'MARYB',         # Mary Borowski
    54: 'JIMB',          # James Bower
    55: 'KAYB',          # Kay Brannen
    56: 'JOHNB',         # John Breed
    57: 'CHARLESB',      # Charles Broskey
    58: 'HELENB',        # Helen Bubenheim
    59: 'SHIRLEYB',      # Shirley Bulava
    60: 'MIKEC',         # Mike Campbell
    61: 'KENC',          # Ken Caroccia
    62: 'LOUISECARR',    # Louise Carr
    63: 'NADINEC',       # Nadine Carter
    64: 'STEVEC',        # Steve Carter
    65: 'SANDICAR',      # Sandi Carvalho
    66: 'ALLANC',        # Allan Clark
    67: 'BETHC',         # Beth Clark
    68: 'RICHARDC',      # Richard Clark
    69: 'MITCHC',        # Mitch Cohen
    70: 'ADRIANC',       # Adrian Cole
    71: 'JIMC',          # Jim Collins
    72: 'JOHNCONT',      # John Conteduca
    73: 'ANASTASIAC',    # Anastasia Crutchfield
    74: 'RAYC',          # Ray Cumba
    75: 'PEGGYC',        # Peggy Cushman
    76: 'NANCYDANS',     # Nancy Dans
    78: 'PATRICIAD',     # Patricia Dennis
    80: 'LARRYD',        # Larry Donahue
    81: 'BOBD',          # Bob Donnelly
    82: 'CECED',         # Cece Donnelly
    83: 'JANED',         # Jane Drake
    84: 'LARRYDR',       # Larry Dreyer
    85: 'JOED',          # Joe Dubel
    86: 'JANE',          # Jan Edwards
    87: 'JIMED',         # Jim Edwards
    88: 'JIME',          # Jim Embree
    89: 'LINDAE',        # Linda Engebretson
    90: 'KASEYE',        # Kasey Englund
    91: 'JIMEN',         # Jim Enlow
    92: 'TONIE',         # Toni Ermini
    93: 'SCOTTIF',       # Scotti Feeley
    94: 'BARRYF',        # Barry Feinblatt
    95: 'MIKEFEF',       # Mike Fefferman
    96: 'RAEFE',         # Rae Fernelius
    97: 'ECF',           # E C Forbes
    98: 'JOF',           # Jo Forbes
    99: 'TERESAF',       # Teresa Frederickson
    100: 'SANDYLYONS',    # Sandy Lyons
    101: 'NANCYG',        # Nancy Geisinger
    102: 'ELAINEGER',     # Elaine German
    103: 'KENGER',        # Ken German
    104: 'WILLG',         # Will Gildner
    105: 'PATG',          # Pat Glass
    106: 'ELLENG',        # Ellen Greenspan
    107: 'LINDAH',        # Linda Habel
    108: 'BOBH',          # Bob Hamilton
    109: 'DIANEH',        # Diane Heath
    110: 'CAROLEH',       # Carole Heierle
    111: 'SHARONHEN',     # Sharon Henriod
    112: 'LEONARDH',      # Leonard Herscovitch
    113: 'FREDH',         # Fred Hinshaw
    114: 'AUDREYH',       # Audrey Holman
    115: 'AASEH',         # Aase Hopkins
    116: 'ELLENH',        # Ellen Hordan
    117: 'CONNIEJ',       # Connie Jackson
    118: 'JERRYJESOR',    # Jerry Jezorski
    119: 'KENJ',          # Ken Johnson
    120: 'CORNELIAK',     # Cornelia Kalender
    121: 'HEINZK',        # Heinz Kalender
    122: 'FREDK',         # Fred Kaplan
    123: 'ANNETTEK',      # Annette Kasson
    124: 'LEEK',          # Lee Kearney
    125: 'JOANK',         # Joan Keltner
    126: 'KATHYK',        # Kathy Kirby
    127: 'JIMK',          # Jim Kindelan
    128: 'WARRENK',       # Warren Knight
    129: 'BILLK',         # Bill Krane
    130: 'JOANKRANE',     # Joan Krane
    131: 'DOUGK',         # Doug Krause
    132: 'NANCYK',        # Nancy Krause
    133: 'LAWRENCEK',     # Lawrence Krenzien
    134: 'THEOK',         # Theo Kurvers
    135: 'LINDAL',        # Linda LaFleur
    136: 'SILVIAL',       # Silvia LaMay
    137: 'WALTL',         # Walter LaMay (duplicate of 31)
    138: 'FRANKL',        # Frank Laverty
    139: 'HARVEYL',       # Harvey Lawrence
    140: 'NORMAL',        # Norma Lawrence
    141: 'DONL',          # Don LeHeup
    142: 'BETHL',         # Beth LeHeup
    143: 'SAMMYL',        # Sammy Liguori
    144: 'RICHARDL',      # Richard Lloyd
    145: 'CATHYL',        # Cathy Lytle
    146: 'JOHNL',         # John Lytle
    149: 'RITAM',         # Riota Maher
    150: 'AUDREYMALE',    # Audrey Malé
    151: 'BETTYMAR',      # Betty Margolis
    152: 'DOLLYM',        # Dolly Marslender
    153: 'JOHNMAR',       # John Marslender
    154: 'BJMAR',         # BJ Martens
    155: 'RAYM',          # Ray Martens
    156: 'CHIYOKOM',      # Chiyoko Matsumoto
    157: 'TAKM',          # Tak Matsumoto
    158: 'JANETM',        # Janet May
    159: 'JOHNMC',        # John McBain
    160: 'TERRYMCM',      # Terry McMullin
    161: 'BILLM',         # Bill Mellis
    162: 'SHARONM',       # Sharon Meyerkamp
    163: 'JEANMIZZI',     # remove
    164: 'HELENM',        # Helen Modrzejewski
    165: 'JEANM',         # Jean Mohler
    166: 'CLIVEM',        # Clive Moniz
    167: 'NANCYM',        # Nancy Montano
    168: 'LOUM',          # Lou Moseley
    169: 'BARBARAM',      # Marbara Morris
    170: 'BILLMUENCH',    # Bill Muench
    171: 'LINDAMUEN',     # Linda Muench
    172: 'CARMENM',       # Carmen Munoz
    173: 'VICKIMUST',     # Vicki Mustard
    174: 'DENNISNIC',     # Dennis Nicpon
    175: 'PATO',          # Pat Oleson
    176: 'JEANO',         # Jean Olson
    177: 'EVELYNO',       # Evelyn Ostis
    178: 'SIDO',          # Sid Ostis
    179: 'BEATRICEP',     # Bea Pagano
    180: 'JACKIEP',       # Jackie Page
    181: 'SUEP',          # Sue Papilion
    182: 'JUNEP',         # June Petrucci
    183: 'WENDELLP',      # Wendell Phillips
    184: 'ARTHURP',       # Arthur Plaggemeier
    185: 'ELKEP',         # Elke Plaggemeier
    186: 'LOUISPOL',      # Lou Polizzotti
    187: 'ROSEMARIEP',    # Rose Marie Princ
    188: 'LARRYQ',        # Larry Quan
    189: 'NORMR',         # Norm Rasmussen
    190: 'DALER',         # Dale Ann Reed
    192: 'KARENRICH',     # Karen Richards
    193: 'VINRICH',       # Vin Richards
    195: 'DONNAR',        # Donna Roskens
    196: 'RUSSR',         # Russ Roskens
    197: 'LINDAR',        # Linda Rosner
    198: 'MURRAYR',       # Murray Rosner
    199: 'GARYROSS',      # Gary Ross
    200: 'JIMROSS',       # Jim Ross
    201: 'PATROSS',       # Pat Ross
    202: 'EULICER',       # Eulice Row
    203: 'DAVIDR',        # David Royer
    204: 'CLEMR',         # Clem Rybacki
    205: 'THADDEUSS',     # Ted Salasavage
    206: 'ALANS',         # Alan Sampsel
    207: 'ANDYS',         # Andy Schizas
    208: 'DIANESCH',      # Diane Schmidt
    209: 'LINS',          # Lin Schmidt
    210: 'BILLS',         # Bill Schoening
    211: 'BILLSE',        # Bill Secrist
    212: 'BOBS',          # Bob Segler
    213: 'MARYS',         # Mary Sgroi
    214: 'JOS',           # Jo Simon
    215: 'NAOMIS',        # Naomi Simonelli
    216: 'REGINES',       # Reggie Skancke
    217: 'GENES',         # Gene Sloboda
    218: 'BILLSOLL',      # Bill Sollars
    219: 'LEAS',          # Lea Solomon
    220: 'OTHAS',         # Otha Spencer-Williams
    221: 'DAVIDST',       # David Stahlhut
    222: 'LINDAS',        # Linda Stahlhut
    223: 'GERIS',         # Geraldean Jeri Stephan
    224: 'ROGERS',        # Roger Stephenson
    225: 'JANSTEW',       # Jane Stewart
    226: 'BOBSW',         # Bob Swanson
    227: 'LOTTIET',       # Lottie Tabor
    228: 'MICHAELT',      # Michael Tanaka
    229: 'GENET',         # Gene Thomas
    230: 'DARLENEV',      # Darlene Vaturi
    231: 'SCOTTV',        # Scott Veaudry
    232: 'DENNISV',       # Dennis Vetter
    233: 'JERREW',        # Jerre Walterscheid
    234: 'MARTINW',       # Martin Weiner
    236: 'SANDRAW',       # Sandra Weiser
    237: 'BRIANW',        # Brian Wells
    238: 'CYNTHIAW',      # Cynthia White
    240: 'CAROLYNW',      # Carolyn Williams
    241: 'JERRYWI',       # Jerry Willick
    242: 'GEORGEW',       # George Winikoff
    243: 'ILENEW',        # Ilene Wong
    244: 'RUSSELLW',      # Russell Wong
    245: 'MIKEW',         # Mike Wuebker
    246: 'CHRISTOPHERZ',  # Christopher Zinn
    247: 'JOHNZUZICH',    # John Zuzich
    248: 'SHIRLEYBALL',   # Shirley Ball
    249: 'JOHNCOOP',      # John Cooper
    250: 'CAROLKAY',      # Carol Kay
    251: 'WILLIAML',      # William Leger
    252: 'PETEO',         # Pete Oleson
    253: 'GEORGEU',       # George Ulrich
    254: 'GINNYU',        # Ginny Ulrich
    255: 'DOROTHYMAC',    # Dorothy Macchio
    257: 'JOECERVA',      # Joe Cerva
    258: 'JUDYCERVA',     # Judy Cerva
    260: 'DICKCOLWELL',   # Dick Colwell
    260: 'KATHRYNF',      # Kathryn Feller
    261: 'SUEGEFF',       # Sue Geffen
    262: 'JEANHEATH',     # Jean Heatherly
    263: 'LASZLOH',       # Laszlo Heredy
    264: 'ROZIH',         # Rozi Heredy
    265: 'MALK',          # Mal Kastroll
    267: 'SANDYL',        # Sandy Levine
    268: 'KENM',          # Ken Mickelson
    269: 'JOHNNICH',      # John Nicholas
    270: 'JOHNNOV',       # John Novicky
    271: 'RONPFEFF',      # Ron Pfeffer
    272: 'JOELLUG',       # Joel Lugavere
    273: 'DONNAP',        # Donna Pfeffer
    274: 'JULIEZ',        # Julie Zerbel
    275: 'JOHNS',         # John Steele
    276: 'PATRICIAS',     # Patricia Steele
    277: 'CYNTHIAB',      # Cynthia Beck
    279: 'JIM SMITH',     # Jim Smith
    280: 'JEANNES',       # Jeanne Swanson
    282: 'JOER',          # Joe Roeder
    283: 'KRISS',         # Kris Steinwand
    284: 'GINGERZ',       # Ginger Zarobsky
    285: 'PATLEM',        # Pat LeMay
    286: 'CLETEM',        # Clete Meyer
    287: 'GREGS',         # Greg Schoo
    290: 'JUDYF',         # Judith Foy
    291: 'NEILB',         # Neil Ballinger
    292: 'MARINELLB',     # Marinell Barber
    293: 'NANCYKO',       # Nancy Koppien
    294: 'GLADYSL',       # Gladys London
    295: 'JOHNWEST',      # John West
    296: 'BRUCEP',        # Bruce Petrie
    297: 'LIZH',          # Elizabeth Harness
    298: 'SUES',          # Sue Strom
    299: 'DIANES',        # Diane Spencer
    300: 'JIMPA',         # Jim Parker
    301: 'LINDAPA',       # Linda Parker
    302: 'EMILYO',        # Emily O'Brien
    303: 'ANNEW',         # Anne Wilson
    304: 'JOSEPHT',       # Joseph Tao
    305: 'ROUSANAT',      # Rousana Tao
    306: 'BRANDONR',      # Brandon Richards
    307: 'BOBRIC',        # Bob Richards
    308: 'PATBR',         # Pat Brunk
    309: 'BARBARAAIM',    # Barbarr Aimone
    310: 'NORMD',         # Norm Derrin
    311: 'LORETTAG',      # Loretta Gonzalez
    312: 'CARLJA',        # Carl Jaumotte
    313: 'GABEC',         # Gabe Centenera
    314: 'DONRUT',        # Don Rutkowski
    315: 'LAURIEHU',      # Laurie Hughes
    316: 'BOBSTELL',      # Bob Stellabott
    317: 'SHIRLEYDO',     # Shirley Domian
    318: 'JIMDOM',        # Jim Domian
    319: 'ARTWI',         # Art Withington
    320: 'ANNETTEWI',     # Annette Withington
    321: 'JANHOH',        # Jan Hohn
    323: 'RICHARDGILL',   # Richard Gillhoover
    324: 'LAURALOU',      # Laura Loughran
    325: 'SUSANHUT',      # Susan Hutchins
    326: 'DONALDD',       # Donald Davidson
    327: 'RONCIN',        # Ron Cinelli
    328: 'ALLETHOM',      # Allen Thomas
    329: 'ROGERMCCOR',    # Roger McCormick
    330: 'MACCORM',       # Keith McCormick
    331: 'TONIMAY',       # Antonia Mayberry
    332: 'EDDIEW',        # Eddie Weininger
    333: 'RENEHIT',       # Rene Hitner
    334: 'NORMANCO',      # Norman Cohen
    335: 'TIMBROOKS',     # Tim Brooks
    336: 'EVIES',         # Evie Scayan
    337: 'JOANNAG',       # Joanna Gorman
    338: 'RAYA',          # Ray Anderson
    339: 'SHELLEYA',      # Shelley Anderson
    340: 'ELAINESEIF',    # Elaine Seifert
    341: 'FLORAM',        # Flora Muskovits
    342: 'MARKZ',         # Mark Zovic
    343: 'PEGGYOWENS',    # Peggy Owens
    344: 'HELENBROWN',    # Helen Brown
    345: 'DOROTHYTOPF',   # Dorothy Topf
    346: 'JACKVINO',      # Jack Vino
    347: 'JULIEF',        # Julie Feist
    348: 'LYNNARNN',      # Lynn Arnn
    349: 'JIMMCC',        # Jim McCall
    350: 'ESTHERWALLS',   # Eshther L. Walls
    351: 'PATSMITH',      # Pat Smith
    352: 'BILLHELM',      # Bill Helm
    353: 'DEANG',         # Dean Grassick
    354: 'SUZANNEP',      # Suzanne Price
    355: 'ANDMELVIL',     # Andrea Melville
    356: 'EVELYNFERG',    # Evelyn Ferguson
    357: 'MAGGIEG',       # Maggie George
    358: 'BILLGEORGE',    # Bill George
    360: 'JUDYPUG',       # Judy Pugmire
    361: 'RUSSTINK',      # Russ Tinkham
    362: 'WILLIEWILCOX',  # Willie Wilcox
    363: 'GENEFAS',       # Gene Fasciana
    364: 'NANSTEVEN',     # Nan Stevenson
    365: 'RAYPUHAL',      # Ray Puhalski
    366: 'DAISYP',        # Daisy Greve
    367: 'GARYR',         # Gary Ranney
    368: 'ELAINEEV',      # Elaine Evenson
    369: 'BILLE',         # Bill Euler
    371: 'JUDYSCH',       # Judy Schmitt
    372: 'HOWARDB',       # Howard Balduc
    374: 'CONNIESI',      # Connie Sieber
    375: 'TOMM',          # Tom Melville
    376: 'DENNISDAG',     # Dennis Daggett
    378: 'BILLMILL',      # Bill Miller
    379: 'TINAS',         # Tina (Josephine) Stephenson
    382: 'BOBF',          # Bob Friegang
    383: 'DIANEF',        # Diane Friegang
    384: 'JOLYNNR',       # Jolynn Reid
    385: 'CAROLTR',       # Carol Trejbal
    386: 'PHILP',         # Philip Pupanek
    387: 'JEANNEMICHEL',  # Jeanne Michel
    388: 'RONG',          # Ron Gangwes
    389: 'JIMWEL',        # Jim Wellman
    390: 'DARRELLHAR',    # Darrell Harness
    392: 'JOANNFERN',     # JoAnn fernstrum
    394: 'GLENCO',        # Glencora Lannen
    395: 'JOHNBACH',      # John Bacher
    396: 'ROBINK',        # Robin King
    397: 'CASEYT',        # Casey Toth
    398: 'DEBL',          # Deb Lamkin
    400: 'SUZANNES',      # Suzanne Sharp
    401: 'GEORGER',       # George Reynolds
    402: 'STEVONS',       # Stevon Stewart
    406: 'JIMMIEL',       # Jimmie Lawson
    407: 'DENNISC',       # Dennis Cavanaugh
    408: 'CONNIEM',       # Connie Moyle
    409: 'DANAL',         # Dana Lakeman
    411: 'EILEENSI',      # Eileen Singer
    412: 'LARRYHA',       # Larry Hanks
    413: 'ALLYNA',        # Allyn Ayotte
    414: 'MINNIEB',       # Minnie Byers
    415: 'MICKID',        # Micki Donch
    416: 'GARYC',         # Gary Cummings
    418: 'HILDAA',        # Hilda Ayotte
    419: 'DEBRALE',       # Debra LeBarts
    420: 'ALANLE',        # Alan LeBarts
    421: 'ROSEMARYW',     # Rosemary Williams
    422: 'LLOYDW',        # Lloyd Williams
    423: 'CHRISB',        # Chris Berthelsen
    424: 'SUZANNESL',     # Suzanne Slater
    425: 'VICTORH',       # Victor Huang
    426: 'CHRISCA',       # Chris Catalone
    427: 'GARYMCD',       # Gary McDougall
    429: 'JOHNMURPHY',    # John Murphy
    430: 'FRANKMI',       # Frank Miyazono
    431: 'PETER RA',      # Peter Raczkiewicz
    432: 'THOMASD',       # Thomas Dennis
    433: 'MITCHF',        # Mitch Fadem
    434: 'LYNDAFELD',     # Lynda Feldman
    435: 'LINDAHEILB',    # Linda Heilbroner
    436: 'ERIKB',         # Erik Braun
    437: 'RICHMO',        # Rich Motycka
    438: 'DEBBIEMO',      # Debbie Motycka
    439: 'FREDMALUEG',    # Fred Malueg
    440: 'ANGIES',        # Angie Smith
    441: 'CATHERINE K',   # Catherine Kostecki
    442: 'BONNYC',        # Bonny Cohen
    444: 'MASSOUDM',      # Massoud Modarres
    445: 'DONNAA',        # Donna Asher
    446: 'TOMMA',         # Tom Malich
    448: 'SHARONN',       # Sharon Neal
    448: 'JAYS',          # Jay Sesto
    449: 'MIKEASHMORE',   # Mike Ashmore
    450: 'LOISL',         # Lois Lewis
    451: 'GARNETW',       # Garnet Wynants
    453: 'BILLHOLDEN',    # Bill Holden
    454: 'DOROTHYDOWN',   # Dorothy Downing
    455: 'LINDAVANH',     # Linda Van Horn
    456: 'RUTHDOD',       # Ruth Dodrill
    457: 'KITTYK',        # Kathleen Koeplin
    458: 'BARBARAMIRMAN', # Barbara Mirman
    459: 'DENISEJOHSON',  # Denise Johnson
    460: 'EILEEN',        # Eileen Cox
    461: 'FREDC',         # Fred Carson
    464: 'HUTCH',         # David Hutchinson
    465: 'HARRYB',        # Harry Blazer
    466: 'DEREKH',        # Derek Hillman
    469: 'DAVEV',         # Dave Vaughan
    470: 'DARV',          # Dar Vaughan
    471: 'BRIANH',        # Brian Heaney
    472: 'FREDHEN',       # Fred Hendrickson
    473: 'NEILBR',        # Neil Braun
    474: 'PHILTAL',       # Phil Talarico
    475: 'JIGRIMM',       # Jimmy Grimm
    476: 'LARRYWEYER',    # Larry Weyers
    477: 'MARKKEYL',      # Mark Keyloun
    478: 'PAULTHOMP',     # Paul Thompson
    479: 'JANETNEW',      # Janet Newton
    480: 'BOBNEWT',       # Bob Newton
    481: 'JIMSTRO',       # Jim Strom
    482: 'MILTGOLD',      # Milt Goldstein
    483: 'DENNIS MULV',   # Dennis Mulvey
    485: 'MARYANNGRIM',   # Mary Ann Grimm
    486: 'ROBMCCLA',      # Rob McClain
    487: 'HELENDAVE',     # Helen Davey
    488: 'CAROLATKINS',   # Carolyn Atkinson
    489: 'BETTYVITT',     # Betty Vittori
    490: 'JOHNWALD',      # John Waldron
    491: 'CHERYLDUNH',    # Cheryl Dunham
    492: 'DAVEFOX',       # Dave Fox
    493: 'CHRISFOX',      # Christine Fox
    494: 'MONIBEUM',      # Monica Beumer
    495: 'DANBEUM',       # Daniel Beumer
    496: 'MARSKLEIN',     # Marsha Klein
    497: 'BRENDACHAL',    # Brenda Chaloupka
    498: 'MELCHAL',       # Mel Chaloupka
    499: 'RICKCORN',      # Rick Cornstuble
    500: 'MIKESTOKE',     # Mike Stokes
    501: 'KAYSTOKE',      # Kay Stokes
    502: 'DEBBIEFRIED',   # Debbie Friedman
    503: 'NEDPERC',       # Ned Percival
    504: 'ELVIRASAN',     # Elvira Santiano
    505: 'GAILMCNA',      # Gail McNamara
    506: 'HARRYMAC',      # Harry Mack
    507: 'JUDITHLEV',     # Judith Levine
    508: 'STEVEDOUG',     # Steve Douglass
    509: 'FLOYDMATHE',    # Floyd Matheny
    510: 'MARYMATHE',     # Mary Matheny
    511: 'JOHNWALK',      # John Walker
    512: 'LINDACOLEM',    # Linda Coleman
    513: 'JOHNCOLEM',     # John Coleman
    514: 'TAIAKIN',       # Tai Akina
    515: 'VERAKINA',      # Verna Akina
    516: 'PHYLGRAN',      # Phyllis Grand
    517: 'LOUIEMED',      # Louie Medrano
    518: 'PRISAMER',      # Priscilla Amerian
    519: 'CATHSWIN',      # Cathy Swindle
    520: 'NADINROB',      # Nadine Robetor
    521: 'BOBSEB',        # Bob Sebastian
    522: 'JOAZORN',       # JoAnn Zornow
    523: 'SOLEGAR',       # Soledad Garcia
    524: 'HERMWEL',       # Herma Wells
    525: 'CONNIELIVE',    # Connie Lively
    526: 'BECKYLOP',      # Becky Lopez
    527: 'CARFRIED',      # Carol Friedman
    528: 'JUDIEBAR',      # Judie Barrett
    529: 'VERONICAD',     # Veronica Douglass
    531: 'JANICEW',       # Janice Wentz
    532: 'LONNIES',       # Lonnie Shannon
    533: 'KITTBJORN',     # Kitt Bjornson
    534: 'STANDSOU',      # Stan Dsouza
    535: 'BRUCESP',       # Bruce Spitzer
    536: 'CECESMI',       # Cecelia Smith
    537: 'FREDBAIL',      # Fred Bailey
    538: 'JANBAIL',       # Janet Bailey
    539: 'MIKECHRI',      # Mike Christiansen
    540: 'SIEWLEE',       # Siew Lee-Rowsell
    541: 'FREDCOM',       # Fred Comes
    542: 'LYDIANOY',      # Lydia Noyola
    543: 'DAVGOLD',       # David Goldhecht
    544: 'MICHPENN',      # Michael Pennock
    545: 'RICHEN',        # Rich Henson
    546: 'MIRIBLOCK',     # Miriam Block
    547: 'DANJOHNST',     # Dan Johnston
    548: 'LYNNHAT',       # Lynn Hatcher
    549: 'JUDHAT',        # Judy Hatcher
    551: 'EARLSTIT',      # Earl Stitt
    552: 'JOEOCON',       # Joe O'Connell
    554: 'SUSGAR',        # Susan Garcia
    555: 'JEFFGR',        # Jeffrey Green
    556: 'JRBAJ',         # JR Bajarias
    558: 'DEBBAN',        # Debbie Bannon
    560: 'TOMJENK',       # Tom Jenks
    561: 'AMBFLEIS',      # Amber Fleisher
    562: 'MISPEC',        # Michael Speciale
    563: 'TERCAR',        # Terry Carey
    564: 'JIMCAR',        # Jim Carey
    565: 'SARGRE',        # Sarah Greene
    566: 'NANCYLUCK',     # Nancy Lucke
    567: 'DARLUCK',       # Daryl Lucke
    568: 'RICLIN',        # Richard Linsmeier
    569: 'BOBMO',         # Bob Monk
    570: 'TSUMEY',        # Tsuneko Meyers
    571: 'MAUMCC',        # Maureen Mc Cartin
    572: 'BECKHERN',      # Becki Hernandez
    573: 'KATCLE',        # Kathleen Clemensen
    574: 'PATSPE',        # Pat Spear
    575: 'ALIENG',        # Ali Engellenner
    576: 'ROBENG',        # Robert Engellenner
    579: 'HARSMI',        # Harry Smith
    580: 'ROBMAH',        # Robert Maher
    581: 'JUNWAN',        # Jun Wei Wang
    582: 'CELWIL',        # Celestia Wilkinson
    583: 'LARWIL',        # Larry Williams
    584: 'JONBRO',        # Jon Brown
    585: 'SUSBRO',        # Susan Brown
    586: 'MARKSTE',       # Mark Stevens
    587: 'RICHWEB',       # Richard Weber
    588: 'RICHBEC',       # Richard Becker
    589: 'JOHNBARR',      # John Barrett
    590: 'CARCLAI',       # Carol Claiborne
    591: 'HARKAP',        # Harry Kaplan
    592: 'JERHOFF',       # Jerry Hoffspiegel
    593: 'LIZDEV',        # Liz Devilbiss
    594: 'PEPINM',        # Pepin Meierhofer
    595: 'SHEKNA',        # Sheri Knaub
    596: 'DAVILL',        # David Illig
    597: 'LAUMAK',        # Lauren Makar
    598: 'MITSWE',        # Mitch Swetsky
    599: 'EDISWE',        # Edith Swetsky
    600: 'KARWIL',        # Kari Wilburn
    601: 'DEBTIL',        # Debbie Tilotti-Kozel
    602: 'RICHMOE',       # Richie Moeller
    603: 'SUESCH',        # Sue Schniepp
    604: 'CYNBLA',        # Cynthia Blake
    605: 'DAVEWIL',       # David Wilson
    606: 'JACKIETH',      # Jackie Thornhill
    607: 'ALDANN',        # Albert Dann
    608: 'ROBGREEN',      # Robert Greene
    610: 'FREDSM',        # Fred Smith
    611: 'JAYGO',         # Jay Goldenberg
    612: 'FRASHOV',       # Frank Shover
    613: 'JOHNSNI',       # John Snipes
    614: 'DAVTHOM',       # Dave Thomas
    615: 'BOBAND',        # Bob Anderson
    616: 'SUSYOU',        # Susan Young
    617: 'GUYCHI',        # Guy Chidiac
    618: 'DEBALE',        # Deborah Alexander
    619: 'GENEK',         # Gene Koch
    620: 'MARYJO',        # Mary Jo Brown
    621: 'PERCAN',        # Perry Cance
    622: 'CATHYDUR',      # Cathy Durant
    623: 'PATWIL',        # Patty Wills
    624: 'TEKASUM',       # Teka Summers
    625: 'SHERCH',        # Sherli Chin
    626: 'CARSTIN',       # Carol Stinnett
    627: 'ALONAS',        # Alona Stephenson
    628: 'HOWSTE',        # Howard Stephenson
    629: 'MARYJU',        # Mary Jane Ursem
    630: 'MELWISE',       # Melanie Wiseman
    631: 'MARKOR',        # Mark O'Rourke
    632: 'FRANKPAT',      # Frank Patino
    633: 'KATLEE',        # Katherine Lee
    634: 'SANKRAU',       # Sandra Krause
    635: 'GEORGEPER',     # George Perkins
    636: 'DORISPER',      # Doris Perkins
    637: 'LITASA',        # Lita Sadorra
    638: 'DONHAMB',       # Don Hamby
    639: 'MIKGAL',        # Michael Galovits
    640: 'PATDAV',        # Patricia Davis
    641: 'PAULLUS',       # Paul Luszcz
    642: 'PATFAIV',       # Patrick Faivre
    643: 'JULKISO',       # Julie Kisosondi
    644: 'MATTKIS',       # Matthew Kisosondi
    646: 'TOMPOST',       # Thomas Post
    647: 'MARCOL',        # Margie Colyer
    648: 'TONTOR',        # Tony Torres
    649: 'MARKPY',        # Mark Pywell
    651: 'JERTAK',        # Jerry Takier
    652: 'DAWNCUN',       # Dawn Cunningham
    653: 'SHERLAS',       # Shirley Laster
    654: 'PAULAND',       # Paula Anderson
    655: 'PETEHAM',       # Pete Hammond
    656: 'LINDASWIT',     # Linda Switzer
    657: 'JEANTAL',       # Jeannette Talarico
    658: 'FREDRAY',       # Fred Ray
    659: 'DORALYNLUKE',   # Doralyn Luke
    660: 'PAULANDER',     # Paul Andersen
    661: 'THERESEAND',    # Therese Andersen
    662: 'MICHELEVANT',   # Michele VanTassell
    663: 'ROBINWOOL',     # Robin Wooley
    664: 'JANETWOOL',     # Janet Wooley
    665: 'STEVEHAN',      # Steve Handelman
    666: 'LORETTASAB',    # Loretta Sabella
    667: 'HELENACUS',     # Helena Cusumano
    669: 'RONMAIM',       # Ron Maimon
    670: 'BOBSHIR',       # Bob Shirai
    672: 'JOANVOR',       # Joanne Vorhies
    673: 'MICHBIRN',      # Michael Birnbaum
    674: 'PAIVOH',        # Paige Vorhies
    675: 'PHIHON',        # Phil Horn
    676: 'NANHOSK',       # Nancy Hoskins
    677: 'JACKHOS',       # Jack Hoskins
    678: 'CAROLJO',       # Caroline Jowers
    679: 'DEBMADRI',      # Deb Madriaga
    680: 'ROSABER',       # Roseanne Berkowitz
    681: 'MILTBERK',      # Milton Berkowitz
    682: 'DUANECL',       # Duane Clement
    683: 'ADELMARCH',     # Adele Marchionda
    684: 'SUSANKIR',      # Susan Kirby
    685: 'DEODOWD',       # Dee O'Dowd
    686: 'VICKYWALK',     # Vicky Walker
    687: 'BARBARACAR',    # Barbara Carson
    688: 'DE ILAMEYER',   # De Ila Meyer
    689: 'DEEDEEKEM',     # DeeDee Kemper
    690: 'ANNMUELL',      # Ann Mueller
    691: 'MARIAMEL',      # Maria Melgarejo
    692: 'MOLLYSHER',     # Molly Sher
    693: 'CATHSUTH',      # Cathy Sutherland
    694: 'BARBLEVY',      # Barbara Levy
    695: 'DANSIMON',      # Dan Simon
    696: 'BOBBORD',       # Bob Bordenave
    697: 'TIBEASLEY',     # Ti Beasley
    698: 'MIKEMAYNE',     # Mike Mayne
    701: 'ALECJOPP',      # Alec Jopp
    702: 'DANIELARM',     # Daniel Armand
    703: 'BOBBYBR',       # Bobby Brauer
    704: 'HERBROLFES',    # Herb Rolfes
    705: 'CONVAN',        # Connie Van Blarcum
    706: 'GARBIE',        # Gary Biederer
    707: 'ROGTOW',        # Roger Townsend
    708: 'BOBBEERS',      # Bob Beers
    709: 'JOANBOW',       # Joan Bower
    710: 'JOSEPHS',       # Joseph Scanlan
    711: 'LYNWORTH',      # Lynn Worthington
    712: 'CHRISOELER',    # Chris Oelerich
    713: 'KATHRYNW',      # Kathryn Wirth
    714: 'SHAVONHAN',     # Shavon Hankins
    715: 'GEORGEFERN',    # George Fernandez
    716: 'BETHWEISS',     # Beth Weissman
    717: 'KARENHEL',      # Karen Helander
    718: 'LARRYIRV',      # Larry Irvine
    719: 'VICKIEBAR',     # Vickie Baroch
    720: 'MARIANDESUM',   # Marian De Sumrak
    721: 'MARSWIT',       # Mary Switzer
    722: 'MARLAG',        # Marla Lagattuta
    723: 'BILLHIPP',      # Bill Hipp
    724: 'RONBROW',       # Ron Brow
    725: 'BONBROW',       # Bonnie Brow
    726: 'KATHCOL',       # Kathy Colton
    727: 'TERMATT',       # Terry Matter
    729: 'JANSCH',        # Janis Schoen
    730: 'JACKSAW',       # Jack Sawatzki
    731: 'CHRISMAN',      # Christine Manion
    732: 'STEVENIC',      # Steven Nicholas
    733: 'SILBAS',        # Silvia Basurto
    735: 'ALEXFOR',       # Alex Fors
    736: 'GARYSM',        # Gary Smith
    737: 'JIMTHO',        # Jim Thompson
    739: 'SHIRLTHOMP',    # Shirley Thompson
    740: 'BILLRICH',      # Bill Richardson
    741: 'BRUCEFRA',      # Bruce Frank
    742: 'BETTLEAD',      # Bettina Leadum
    743: 'CINDYSCOTT',    # Cindy Scott
    744: 'ERICHA',        # Eric Hahn
    745: 'LINNGU',        # Linda Nguyen
    746: 'CHRISTINELU',   # Christine Lu
    747: 'RANZHANG',      # Ran Zhang
    748: 'KATHDIS',       # Kathy Disabato
    749: 'DALEDIS',       # Dale Disabato
    750: 'RICHVASQ',      # Richard Vasquez
    751: 'SOFCAST',       # Sofia Castille
    752: 'CORINGON',      # Corina Gonzalez
    753: 'RAULGON',       # Raul Gonzalez
    754: 'TEDDY',         # Ted Dyer
    755: 'STEVMEH',       # Steve Mehling
    756: 'GLOELM',        # Gloria Elmore
    757: 'PAMCON',        # Pam Conboy
    758: 'SUSANEME',      # Susan Emerson
    759: 'JOETUNK',       # Joe Tunkel
    760: 'ROYBERG',       # Roy Berger
    761: 'JERRYFORD',     # Jerry Ford
    763: 'LYNNWOLFE',     # Lynn Wolfe
    764: 'JANROUT',       # Janice Routh
    765: 'DAVGRAY',       # David Gray
    766: 'MARYANNM',      # Mary Ann Massey
    767: 'MARYBASHIST',   # Mary Bashist
    769: 'SANCOL',        # Sandy Collette
    770: 'TIMLETO',       # Tim Letouzel
    771: 'JOHNHOW',       # John Howland
    772: 'FRANFOS',       # Frank Fosco
    773: 'EDDMAL',        # Eddie Maloney
    774: 'JOSVAM',        # Joshua Vampan
    775: 'MARKWE',        # Mark West
    776: 'KIMJEN',        # Kim Jensen
    777: 'DAVPHI',        # David Phillips
    778: 'MARFRAN',       # Marcia Frank
    779: 'MARYENG',       # Mary Engle
    780: 'DAVIDPEL',      # David Peled
    781: 'JOHNVO',        # John Vosicky
    782: 'KATVOS',        # Kathi Vosicky
    783: 'RANDYG',        # Randy Gast
    784: 'PATTIM',        # Patti Malczewski
    786: 'KEVHAW',        # Kevin Hawley
    787: 'MAYTAH',        # May Tahmassebi
    789: 'JANFISC',       # Jan Fischer
    792: 'GLENNG'         # Glenn Goodale
}
#   328: 'ALLENT',        # Allen Thomas
#   355: 'ANDREAM',       # Andrea Melville
#   154: 'BJM',           # B. J. Martens
#   154: 'BJMARTENS',     # B. J. Martens
#   309: 'BARBARAA',      # Barbara Aimone
#     1: 'BARBDOR',       # Barbara Dorway
#   576: 'BOBE',          # Bob Engellenner
#   569: 'BOBM',          # Bob Monk
#   703: 'BOBY',          # Bobby Brauer
#   622: 'CATHDUR',       # Cathy Durand
#   695: 'DANS',          # Dan Simon
#   702: 'DANIEL ARMAND', # Danielarm
#     6: 'DAVEDOR',       # David Dorway
#    68: 'DICKC',         # Dick Clark
#   368: 'ELAINEE',       # Elaine Evenson
#   102: 'ELAINEG',       # Elaine German
#   772: 'FRANKF',        # Frank Fosco
#   636: 'GEORGEP',       # George Perkins
#   617: 'GUYC',          # Guy Chidiac
#   759: 'JOET',          # Joe Tunkel
#   133: 'LARRYK',        # Larry Kernzien
#   315: 'LAURIEH',       # Laurie Hughes
#   512: 'LINCOLE',       # Linda Coleman
#    89: 'LINDAENG',      # Linda Engebretson
#   171: 'LINDAM',        # Linda Muench
#   763: 'LWOLFE',        # Lynn Wolfe
#    95: 'MIKEFEFFER',    # Mike Fefferman
#   711: 'WORTHLYNN',     # Lynn Worthington
#   775: 'MARWES',        # Mark West
#   766: 'MMASSEY',       # MaryAnn Massey
#   621: 'PERRYC',        # Perry Cance
#   231: 'SCOTTVEA',      # Scott Veaudry

#   999: 'ALETHAM',       # Angie Letham
#   999: 'ALLANB',        # remove
#   999: 'ANNETTEL',      # remove
#   999: 'APFELH',        # remove
#   999: 'ARLENEB',       # remove
#   999: 'ARNOLDB',       # remove
#   999: 'ARTL',          # remove
#   999: 'ASHEJANE',      # remove
#   999: 'ASHEJOE',       # remove
#   999: 'AUDREYS',       # remove
#   999: 'BARBARAT',      # remove
#   999: 'BARRJ',         # remove
#   999: 'BARRL',         # remove
#   999: 'BERNARDM',      # remove
#   999: 'BETTYAL',       # Remove
#   999: 'BETTYJ',        # remove
#   999: 'BETTYL',        # remove
#   999: 'BETTYP',        # remove
#   999: 'BILLVIC',       # remove
#   999: 'BOBALTO',       # Remove
#   999: 'BOBBIEF',       # Remove
#   999: 'BOBP',          # remove
#   999: 'BOROWSKIM',     # remove
#   999: 'BRENDAT',       # Remove
#   999: 'BYRONK',        # Remove
#   999: 'CAROLEG',       # Remove
#   999: 'CHARLESCO',     # remove
#   999: 'CHARLESL',      # remove
#   999: 'CHENL',         # remove
#   999: 'CHUCKC',        # Remove
#   999: 'CONTENDUCAJ',   # remove
#   999: 'DARRYLB',       # remove
#   999: 'DAVIDK',        # remove
#   999: 'DAVIDSL',       # remove
#   999: 'DAVIDSTI',      # remove
#   999: 'DENNISK',       # remove
#   999: 'DONC',          # removed
#   999: 'DOROTHYH',      # remove
#   999: 'DOTTYMAR',      # remove
#   999: 'EDG',           # Remove
#   999: 'EDW',           # remove
#   999: 'EDWINHEN',      # remove
#   999: 'EDWINW',        # remove
#   999: 'ELENIK',        # remove
#   999: 'ESTELLEH',      # Remove
#   999: 'ESTHERS',       # remove
#   999: 'FAINGOLDJ',     # remove
#   999: 'FELIXF',        # remove
#   999: 'FELLERK',       # remove
#   999: 'FRANKC',        # remove
#   999: 'FRANKCO',       # REMOVED
#   999: 'FRANKE',        # remove
#   999: 'FREDACRI',      # Fred Acri
#   999: 'GARETTN',       # remove
#   999: 'GARYABEL',      # Gary Abelson
#   999: 'GERALDINEG',    # Remove
#   999: 'GERALDP',       # REMOVE
#   999: 'GERALDS',       # remove
#   999: 'GERIMCE',       # Remove
#   999: 'GLENDAL',       # remove
#   999: 'GLORIANIC',     # remove
#   999: 'GWENS',         # Remove
#   999: 'HENRYP',        # Removed
#   999: 'HIRAML',        # remove
#   999: 'HOLMESS',       # remove
#   999: 'HYL',           # remove
#   999: 'IRENEW',        # remove
#   999: 'IRISM',         # remove
#   999: 'JAMESM',        # Remove
#   999: 'JANB',          # Remove
#   999: 'JANEC',         # remove
#   999: 'JEANB',         # Remove
#   999: 'JEANW',         # remove
#   999: 'JERRY NY',      # remove
#   999: 'JERRYK',        # Remove
#   999: 'JERRYM',        # remove
#   999: 'JERRYS',        # remove
#   999: 'JERRYW',        # remove
#   999: 'JIMKUEHL',      # remove
#   999: 'JIMS',          # Remove
#   999: 'JOANNER',       # Remove
#   999: 'JOANP',         # remove
#   999: 'JOEASHE',       # removed
#   999: 'JOEC',          # Joe Connors
#   999: 'JOHNEB',        # remove
#   999: 'JOHNP',         # remove
#   999: 'JOHNR',         # remove
#   999: 'JOSEPHW',       # remove
#   999: 'JOSETTEF',      # remove
#   999: 'JOYCEC',        # Remove
#   999: 'JUDIEK',        # remove
#   999: 'JUDITHR',       # remove
#   999: 'JUDYG',         # Remove
#   999: 'KARENPET',      # Remove
#   999: 'KASTROLLM',     # Remove
#   999: 'KATHIM',        # remove
#   999: 'KATHYLYONS',    # remove
#   999: 'KENR',          # remove
#   999: 'LEIGHG',        # Remove
#   999: 'LINDAF',        # remove
#   999: 'LINDAFITZ',     # remove
#   999: 'LOUFORT',       # remove
#   999: 'LOUISD',        # remove
#   999: 'LYNDACAR',      # remove
#   999: 'LYNNEB',        # Remove
#   999: 'MANNYA',        # Remove
#   999: 'MARGARETC',     # REMOVE
#   999: 'MARGEBR',       # remove
#   999: 'MARGIEA',       # Margie Abelson
#   999: 'MARTHAG',       # Remove
#   999: 'MARTINJ',       # Remove
#   999: 'MARYF',         # remove
#   999: 'MAXR',          # remove
#   999: 'MILESG',        # Remove
#   999: 'MORTO',         # remove
#   999: 'MURRAYW',       # remove
#   999: 'MYRONG',        # Remove
#   999: 'NICKIR',        # remove
#   999: 'NORLEYS',       # remove
#   999: 'NORMW',         # remove
#   999: 'NYIRIJ',        # remove
#   999: 'PAMROSS',       # remove
#   999: 'PAULM',         # 
#   999: 'PEDROH',        # remove
#   999: 'PRINE R',       # Remove
#   999: 'QTANAKA',       # remove
#   999: 'RALPHM',        # Remove
#   999: 'REXD',          # remove
#   999: 'RICHARDRAN',    # remove
#   999: 'RICHARDWIL',    # Remove
#   999: 'ROBERTH',       # remove
#   999: 'ROBERTR',       # Remove
#   999: 'ROBERTS',       # remove
#   999: 'ROGERW',        # remove
#   999: 'ROSSR',         # remove
#   999: 'SANDYG',        # remove
#   999: 'SANDYV',        # Remove
#   999: 'SHARONABRA',    # remove
#   999: 'SHIRLEET',      # remove
#   999: 'SIMONH',        # remove
#   999: 'STANLEYR',      # remove
#   999: 'STANLEYW',      # removed
#   999: 'SUEEB',         # Remove
#   999: 'SUSANPOL',      # remove
#   999: 'TERIV',         # remove
#   999: 'TIMK',          # remove
#   999: 'TOMB',          # Remove
#   999: 'TOMBURT',       # Tom Burt
#   999: 'TOMK',          # Remove
#   999: 'TOMW',          # remove
#   999: 'VELMAL',        # Remove
#   999: 'VINCENTM',      # remove
#   999: 'VINCENTP',      # remove
#   999: 'VINCES',        # remove
#   999: 'VIRGILB',       # Remove
#   999: 'VLASTAB',       # Remove
#   999: 'WANDAK',        # remove


def format_telephone_number(in_string):
    """
    Strip non-digits and format telephone number
    We assum all numbers are in the NADA and add
    "702-" (Clark County, Nevada) to 7 digit numbers.
    Numbers that are not 7 or 10 digits are returned
    with non-digits stripped but not formatted.
    """

    if in_string is None:
        return(None)
    res = re.sub(r'[^0-9]', '', in_string)
    if len(res) == 7:
        res = "702" + res
    if len(res) == 10:
        res = f"{res[0:3]}-{res[3:6]}-{res[6:]}"
    return(res)


class HTMLFilter(HTMLParser):
    text = ""
    def handle_data(self, data):
        self.text += data + " "


class MemberDB():
    """
    A class to manage the old MemberDB
    """
    # All functions and methods must return date time values as
    # datetime objects.  They must accept date time as datetime
    # objects and convert to the database native format.

    def __init__(self, cmn):
        logging.debug("Init db_member.MemberDB")
        self.cmn = cmn

    def get_active_members(self):
        """Return a dictionary with id:full_name"""

        sql_statement = """
            SELECT Members.MemberID, LastName, FirstName, PrefName
            FROM Members INNER JOIN Service
                ON (Members.MemberID = Service.MemberID)
            WHERE Service.DateDropped IS NULL
                OR (Service.DateRejoined IS NOT Null
                AND Service.DateRedropped IS NULL)"""
#       print(sql_statement)
#       print()
        self.curs_member.execute(sql_statement)
        name_dict = {}
        rows = self.curs_member.fetchall()
        for i in rows:
            name_dict[i.MemberID] = common.display_name(
                i.LastName, i.FirstName, i.PrefName)
        return name_dict

    def get_members(self):
        """Return a list of Member objects"""

        sql_statement = """
            SELECT MemberID, LastName, FirstName, PrefName, Birthday,
                `Deceased?`, DrLicenseNo, DLState, DrExpiryDate, CellPhone,
                HomePhone, `E-Mail`, MAddress, City, State, ZIP, AssociationNo,
                `Renter?`, LeaseExpDate, Notes, DHRdate
            FROM Members"""
#       print(sql_statement)
#       print()
        self.curs_member.execute(sql_statement)
        members = []
        rows = self.curs_member.fetchall()
        for i in rows:
            m = common.Member()
            m.member_id = i.MemberID
            try:
                m.user_name_logdb = member_dict[m.member_id]
            except KeyError:
                m.user_name_logdb = ""
            m.surname = i.LastName
            m.given_name = i.FirstName
            m.nickname = i.PrefName
            m.birthdate = i.Birthday
            m.deceased = i[5] # Deceased?
            m.dl_number = i.DrLicenseNo
            m.dl_state_code = i.DLState
            m.dl_expiry_date = i.DrExpiryDate
#           if not isinstance(m.birthday, datetime.datetime):
#           if m.member_id > 780 or m.surname == "Scanlan":
#               print(f"{m.member_id}:  {m.surname}, {m.given_name}")
            m.telephone_number = []
            # Telephone numberes in the source data need a little
            # cleaning up:
            #     * strip non-digit caracters,
            #     * prepend "702" to 7 digit numbers,
            #     * format strings as "999-999-9999".
            cell = None
            if i.CellPhone:
#               print(m.member_id, i.CellPhone)
                cell = common.TelephoneNumber()
                cell.phone_type = 1 # Mobile/Cell
                cell.phone_number = format_telephone_number(i.CellPhone)
                m.telephone_number.append(cell)
            if i.HomePhone:
                home = common.TelephoneNumber()
                home.phone_type = 2 # Home
                home.phone_number = format_telephone_number(i.HomePhone)
                if cell:
                    if cell.phone_number != home.phone_number:
                        m.telephone_number.append(home)
                else:
                    m.telephone_number.append(home)
            m.email_address = []
            if i[11]:	# E-mail
                home = common.EmailAddress()
                home.email_type = 2 # Home
                home.email_addr = i[11] # E-mail
                m.email_address.append(home)
            m.physical_address = []
            if i.MAddress or i.City or i.State or i.ZIP or i.AssociationNo:
                home = common.PhysicalAddress()
                home.phys_addr_type = 1 # SCSCAI address
                home.postal_code = i.ZIP
                home.state_code = i.State
                home.city_name = i.City
                if i.MAddress:
                    m_address = i.MAddress.split(maxsplit=1)
                    if m_address[0].isdigit():
                        home.street_number = m_address[0]
                        home.street_name = m_address[1]
                    else:
                        home.street_number = None
                        home.street_name = i.MAddress
                home.scscai_number = i.AssociationNo
                home.renter = i[17] # Renter?
                home.lease_expiry_date = i.LeaseExpDate
                m.physical_address.append(home)
            m.member_notes = []
            if i.Notes:
                n = common.MemberNotes()
                f = HTMLFilter()
                f.feed(i.Notes)
                n.member_note = f.text.strip()
                m.member_notes.append(n)
            m.dl_history = []
            if i.DHRdate:
                n = common.DLHistory()
                n.dl_history_date = i.DHRdate
                n.dl_history_note = ""
                m.dl_history.append(n)

            members.append(m)
        return members

    def open_member_db(self):
        """Open Database used by Brian Dodd's applications"""

        try:
            import pyodbc
            conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                r'DBQ=' + self.cmn.stns.get_pathname_member_db() + r';'
                r'Mode=Read;')
            logging.info("    connected to %s", conn_str)
            self.conn_member = pyodbc.connect(conn_str)
            self.curs_member = self.conn_member.cursor()
            return conn_str
        except:
            return None

if __name__ == '__main__':
    cmn = common.Common()
    d = MemberDB(cmn)

    d.open_member_db()
    print()
    print('Member DB')
    print('### Tables:')
    for i in d.curs_member.tables(tableType='TABLE'):
        print(i.table_name)
    print('### Views:')
    for i in d.curs_member.tables(tableType='VIEW'):
        print(i.table_name)

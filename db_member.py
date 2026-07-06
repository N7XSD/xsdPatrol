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
    7: 'DAVIDS',        # David Steinman
    8: 'ELLENB',        # Ellen Bachman
    13: 'BRIAND',        # Brian Dodd
    16: 'JENNIED',       # Jennie Dodd
    17: 'JUDYH',         # Judy Hunt
    21: 'JIMDUN',        # Jim Dunbar
    22: 'NANCYDUN',      # Nancy Dunbar
    27: 'JANETMOS',      # Janet Moseley
    29: 'MARYJOR',       # Mary Jo Richards
    31: 'WALTL',         # Walter LaMay (duplicate of 137)
    35: 'TOMA',          # Tom Amenta
    37: 'BURTA',         # Burt Arnold
    38: 'JANEASHE',      # Jane Ashe
    40: 'RICHARDA',      # Richard Augulis
    43: 'LARRYB',        # Larry Bacon
    50: 'MARYBIRD',      # Mary Bird
    52: 'JERRYB',        # Jerry Borowski
    53: 'MARYB',         # Mary Borowski
    54: 'JIMB',          # James Bower
    56: 'JOHNB',         # John Breed
    57: 'CHARLESB',      # Charles Broskey
    58: 'HELENB',        # Helen Bubenheim
    59: 'SHIRLEYB',      # Shirley Bulava
    65: 'KENC',          # Ken Caroccia
    66: 'ALLANC',        # Allan Clark
    67: 'BETHC',         # Beth Clark
    68: 'RICHARDC',      # Richard Clark
    70: 'ADRIANC',       # Adrian Cole
    71: 'JIMC',          # Jim Collins
    75: 'PEGGYC',        # Peggy Cushman
    76: 'NANCYDANS',     # Nancy Dans
    78: 'PATRICIAD',     # Patricia Dennis
    81: 'BOBD',          # Bob Donnelly
    83: 'JANED',         # Jane Drake
    84: 'LARRYDR',       # Larry Dreyer
    86: 'JANE',          # Jan Edwards
    87: 'JIMED',         # Jim Edwards
    88: 'JIME',          # Jim Embree
    89: 'LINDAE',        # Linda Engebretson
    90: 'KASEYE',        # Kasey Englund
    94: 'BARRYF',        # Barry Feinblatt
    95: 'MIKEFEF',       # Mike Fefferman
    96: 'RAEFE',         # Rae Fernelius
    97: 'ECF',           # E C Forbes
    98: 'JOF',           # Jo Forbes
    100: 'SANDYLYONS',    # Sandy Lyons
    101: 'NANCYG',        # Nancy Geisinger
    102: 'ELAINEGER',     # Elaine German
    103: 'KENGER',        # Ken German
    105: 'PATG',          # Pat Glass
    107: 'LINDAH',        # Linda Habel
    110: 'CAROLEH',       # Carole Heierle
    111: 'SHARONHEN',     # Sharon Henriod
    113: 'FREDH',         # Fred Hinshaw
    114: 'AUDREYH',       # Audrey Holman
    117: 'CONNIEJ',       # Connie Jackson
    119: 'KENJ',          # Ken Johnson
    120: 'CORNELIAK',     # Cornelia Kalender
    122: 'FREDK',         # Fred Kaplan
    124: 'LEEK',          # Lee Kearney
    125: 'JOANK',         # Joan Keltner
    126: 'KATHYK',        # Kathy Kirby
    128: 'WARRENK',       # Warren Knight
    131: 'DOUGK',         # Doug Krause
    132: 'NANCYK',        # Nancy Krause
    133: 'LAWRENCEK',     # Lawrence Krenzien
    134: 'THEOK',         # Theo Kurvers
    136: 'SILVIAL',       # Silvia LaMay
    137: 'WALTL',         # Walter LaMay (duplicate of 31)
    138: 'FRANKL',        # Frank Laverty
    141: 'DONL',          # Don LeHeup
    142: 'BETHL',         # Beth LeHeup
    143: 'SAMMYL',        # Sammy Liguori
    144: 'RICHARDL',      # Richard Lloyd
    145: 'CATHYL',        # Cathy Lytle
    146: 'JOHNL',         # John Lytle
    151: 'BETTYMAR',      # Betty Margolis
    154: 'BJMAR',         # BJ Martens
    155: 'RAYM',          # Ray Martens
    156: 'CHIYOKOM',      # Chiyoko Matsumoto
    157: 'TAKM',          # Tak Matsumoto
    161: 'BILLM',         # Bill Mellis
    162: 'SHARONM',       # Sharon Meyerkamp
    163: 'JEANMIZZI',     # remove
    164: 'HELENM',        # Helen Modrzejewski
    165: 'JEANM',         # Jean Mohler
    168: 'LOUM',          # Lou Moseley
    170: 'BILLMUENCH',    # Bill Muench
    171: 'LINDAMUEN',     # Linda Muench
    174: 'DENNISNIC',     # Dennis Nicpon
    175: 'PATO',          # Pat Oleson
    176: 'JEANO',         # Jean Olson
    180: 'JACKIEP',       # Jackie Page
    183: 'WENDELLP',      # Wendell Phillips
    184: 'ARTHURP',       # Arthur Plaggemeier
    185: 'ELKEP',         # Elke Plaggemeier
    188: 'LARRYQ',        # Larry Quan
    196: 'RUSSR',         # Russ Roskens
    197: 'LINDAR',        # Linda Rosner
    198: 'MURRAYR',       # Murray Rosner
    200: 'JIMROSS',       # Jim Ross
    201: 'PATROSS',       # Pat Ross
    202: 'EULICER',       # Eulice Row
    204: 'CLEMR',         # Clem Rybacki
    205: 'THADDEUSS',     # Ted Salasavage
    210: 'BILLS',         # Bill Schoening
    213: 'MARYS',         # Mary Sgroi
    214: 'JOS',           # Jo Simon
    216: 'REGINES',       # Reggie Skancke
    219: 'LEAS',          # Lea Solomon
    220: 'OTHAS',         # Otha Spencer-Williams
    221: 'DAVIDST',       # David Stahlhut
    222: 'LINDAS',        # Linda Stahlhut
    223: 'GERIS',         # Geraldean Jeri Stephan
    224: 'JANSTEW',       # Jane Stewart
    226: 'BOBSW',         # Bob Swanson
    227: 'LOTTIET',       # Lottie Tabor
    230: 'DARLENEV',      # Darlene Vaturi
    231: 'SCOTTV',        # Scott Veaudry
    236: 'SANDRAW',       # Sandra Weiser
    245: 'MIKEW',         # Mike Wuebker
    246: 'CHRISTOPHERZ',  # Christopher Zinn
    247: 'JOHNZUZICH',    # John Zuzich
    250: 'CAROLKAY',      # Carol Kay
    251: 'WILLIAML',      # William Leger
    255: 'DOROTHYMAC',    # Dorothy Macchio
    257: 'JOECERVA',      # Joe Cerva
    258: 'JUDYCERVA',     # Judy Cerva
    260: 'DICKCOLWELL',   # Dick Colwell
    260: 'KATHRYNF',      # Kathryn Feller
    262: 'JEANHEATH',     # Jean Heatherly
    263: 'LASZLOH',       # Laszlo Heredy
    264: 'ROZIH',         # Rozi Heredy
    267: 'SANDYL',        # Sandy Levine
    271: 'RONPFEFF',      # Ron Pfeffer
    272: 'JOELLUG',       # Joel Lugavere
    273: 'DONNAP',        # Donna Pfeffer
    274: 'JULIEZ',        # Julie Zerbel
    275: 'JOHNS',         # John Steele
    276: 'PATRICIAS',     # Patricia Steele
    277: 'CYNTHIAB',      # Cynthia Beck
    279: 'JIM SMITH',     # Jim Smith
    283: 'KRISS',         # Kris Steinwand
    284: 'GINGERZ',       # Ginger Zarobsky
    287: 'GREGS',         # Greg Schoo
    290: 'JUDYF',         # Judith Foy
    295: 'JOHNWEST',      # John West
    296: 'BRUCEP',        # Bruce Petrie
    297: 'LIZH',          # Elizabeth Harness
    298: 'SUES',          # Sue Strom
    303: 'ANNEW',         # Anne Wilson
    304: 'JOSEPHT',       # Joseph Tao
    305: 'ROUSANAT',      # Rousana Tao
    309: 'BARBARAAIM',    # Barbarr Aimone
    313: 'GABEC',         # Gabe Centenera
    314: 'DONRUT',        # Don Rutkowski
    318: 'JIMDOM',        # Jim Domian
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
    395: 'JOHNBACH',      # John Bacher
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
    710: 'JOSEPHS',       # Joseph Scanlan
    711: 'LYNWORTH'       # Lynn Worthington
}
#   999: 'LINDAENG',      # Linda Engebretson
#   999: 'LINCOLE',       # Linda Coleman

#   999: 'AASEH',         # remove
#   999: 'ADELMARCH',     # Adele Marchionda
#   999: 'ALANS',         # Remove
#   999: 'ALDANN',        # Albert Dann
#   999: 'ALECJOPP',      # Alec Jopp
#   999: 'ALETHAM',       # Angie Letham
#   999: 'ALEXFOR',       # Alex Fors
#   999: 'ALIENG',        # Ali Engellenner
#   999: 'ALLANB',        # remove
#   999: 'ALLENT',        # Remove
#   999: 'ALONAS',        # Alona Stephenson
#   999: 'AMBFLEIS',      # Amber Fleisher
#   999: 'ANASTASIAC',    # remove
#   999: 'ANDREAM',       # Remove
#   999: 'ANDYS',         # Remove
#   999: 'ANNEG',         # remove
#   999: 'ANNETTEK',      # remove
#   999: 'ANNETTEL',      # remove
#   999: 'ANNETTEWI',     # remove
#   999: 'ANNMUELL',      # Ann Mueller
#   999: 'APFELH',        # remove
#   999: 'ARLENEB',       # remove
#   999: 'ARNOLDB',       # remove
#   999: 'ARTL',          # remove
#   999: 'ARTWI',         # remove
#   999: 'ASHEJANE',      # remove
#   999: 'ASHEJOE',       # remove
#   999: 'AUDREYMALE',    # remove
#   999: 'AUDREYS',       # remove
#   999: 'BARBARAA',      # remove
#   999: 'BARBARACAR',    # Barbara Carson
#   999: 'BARBARAM',      # Remove
#   999: 'BARBARAT',      # remove
#   999: 'BARBDOR',       # Barbara Dorway
#   999: 'BARBLEVY',      # Barbara Levy
#   999: 'BARRJ',         # remove
#   999: 'BARRL',         # remove
#   999: 'BEATRICEP',     # Remove
#   999: 'BECKHERN',      # Becki Hernandez
#   999: 'BERNARDM',      # remove
#   999: 'BETHWEISS',     # Beth Weissman
#   999: 'BETTLEAD',      # Bettina Leadum
#   999: 'BETTYAL',       # Remove
#   999: 'BETTYJ',        # remove
#   999: 'BETTYL',        # remove
#   999: 'BETTYP',        # remove
#   999: 'BILLHIPP',      # Bill Hipp
#   999: 'BILLK',         # remove
#   999: 'BILLRICH',      # Bill Richardson
#   999: 'BILLSE',        # remove
#   999: 'BILLSOLL',      # remove
#   999: 'BILLVIC',       # remove
#   999: 'BJM',           # remove
#   999: 'BJMARTENS',     # remove
#   999: 'BOBALTO',       # Remove
#   999: 'BOBAND',        # Bob Anderson
#   999: 'BOBBEERS',      # Bob Beers
#   999: 'BOBBIEF',       # Remove
#   999: 'BOBBORD',       # Bob Bordenave
#   999: 'BOBBYBR',       # Bobby Brauer
#   999: 'BOBE',          # remove
#   999: 'BOBH',          # remove
#   999: 'BOBM',          # remove
#   999: 'BOBMO',         # Bob Monk
#   999: 'BOBP',          # remove
#   999: 'BOBRIC',        # remove
#   999: 'BOBS',          # Bob Segler
#   999: 'BOBSHIR',       # Bob Shirai
#   999: 'BOBSTELL',      # Remove
#   999: 'BOBY',          # remove
#   999: 'BONBROW',       # Bonnie Brow
#   999: 'BOROWSKIM',     # remove
#   999: 'BRANDONR',      # remove
#   999: 'BRENDAT',       # Remove
#   999: 'BRIANW',        # remove
#   999: 'BRUCEFRA',      # BRUCE FRANK
#   999: 'BYRONK',        # Remove
#   999: 'CARCLAI',       # Carol Claiborne
#   999: 'CARLJA',        # Remove
#   999: 'CARMENM',       # Remove
#   999: 'CAROLA',        # Remove
#   999: 'CAROLEG',       # Remove
#   999: 'CAROLJO',       # Caroline Jowers
#   999: 'CAROLYNW',      # remove
#   999: 'CARSTIN',       # Carol Stinnett
#   999: 'CATHDUR',       # Cathy Durand
#   999: 'CATHSUTH',      # Cathy Sutherland
#   999: 'CATHYDUR',      # Cathy Durant
#   999: 'CECED',         # remove
#   999: 'CELWIL',        # Celestia Wilkinson
#   999: 'CHARLESCO',     # remove
#   999: 'CHARLESL',      # remove
#   999: 'CHENL',         # remove
#   999: 'CHRISMAN',      # Christine Manion
#   999: 'CHRISOELER',    # Chris Oelerich
#   999: 'CHRISTINELU',   # Christine Lu
#   999: 'CHUCKC',        # Remove
#   999: 'CINDYSCOTT',    # Cindy Scott
#   999: 'CLETEM',        # Remove
#   999: 'CLIVEM',        # remove
#   999: 'CONNIED',       # remove
#   999: 'CONNIESI',      # Connie Sieber
#   999: 'CONTENDUCAJ',   # remove
#   999: 'CONVAN',        # Connie Van Blarcum
#   999: 'CORINGON',      # Corina Gonzalez
#   999: 'CYNBLA',        # Cynthia Blake
#   999: 'CYNTHIAW',      # Remove
#   999: 'DALEDIS',       # Dale Disabato
#   999: 'DALER',         # remove
#   999: 'DANB',          # remove
#   999: 'DANIEL ARMAND', # Danielarm
#   999: 'DANIELARM',     # Daniel Armand
#   999: 'DANIELLEL',     # Remove
#   999: 'DANS',          # remove
#   999: 'DANSIMON',      # Dan Simon
#   999: 'DARLUCK',       # Daryl Lucke
#   999: 'DARRYLB',       # remove
#   999: 'DAVEDOR',       # David Dorway
#   999: 'DAVEWIL',       # David Wilson
#   999: 'DAVGRAY',       # David Gray
#   999: 'DAVIDDOR',      # David Dorway
#   999: 'DAVIDK',        # remove
#   999: 'DAVIDPEL',      # David Peled
#   999: 'DAVIDR',        # David Royer
#   999: 'DAVIDSL',       # remove
#   999: 'DAVIDSTI',      # remove
#   999: 'DAVILL',        # David Illig
#   999: 'DAVPHI',        # David Phillips
#   999: 'DAVTHOM',       # Dave Thomas
#   999: 'DAWNCUN',       # Dawn Cunningham
#   999: 'DE ILAMEYER',   # De Ila Meyer
#   999: 'DEBALE',        # Deborah Alexander
#   999: 'DEBBAN',        # Debbie Bannon
#   999: 'DEBMADRI',      # Deb Madriaga
#   999: 'DEBTIL',        # Debbie Tilotti-Kozel
#   999: 'DEEDEEKEM',     # DeeDee Kemper
#   999: 'DENNISK',       # remove
#   999: 'DENNISV',       # remove
#   999: 'DEODOWD',       # Dee O'Dowd
#   999: 'DIANEH',        # Remove
#   999: 'DIANES',        # remove
#   999: 'DIANESCH',      # Remove
#   999: 'DICKA',         # Remove
#   999: 'DICKC',         # remove
#   999: 'DOLLYM',        # remove
#   999: 'DONC',          # removed
#   999: 'DONHAMB',       # Don Hamby
#   999: 'DONNAA',        # Donna Asher
#   999: 'DONNAR',        # remove
#   999: 'DORALYNLUKE',   # Doralyn Luke
#   999: 'DORISPER',      # Doris Perkins
#   999: 'DOROTHYH',      # remove
#   999: 'DOTTYMAR',      # remove
#   999: 'DUANECL',       # Duane Clement
#   999: 'EARLSTIT',      # Earl Stitt
#   999: 'EDDMAL',        # Eddie Maloney
#   999: 'EDG',           # Remove
#   999: 'EDISWE',        # Edith Swetsky
#   999: 'EDW',           # remove
#   999: 'EDWINHEN',      # remove
#   999: 'EDWINW',        # remove
#   999: 'ELAINEE',       # Remove
#   999: 'ELAINEG',       # remove
#   999: 'ELENIK',        # remove
#   999: 'ELLENG',        # Remove
#   999: 'ELLENH',        # Remove
#   999: 'EMILYO',        # remove
#   999: 'ERICHA',        # Eric Hahn
#   999: 'ERNIEM',        # remove
#   999: 'ESTELLEH',      # Remove
#   999: 'ESTHERS',       # remove
#   999: 'EVELYNO',       # remove
#   999: 'FAINGOLDJ',     # remove
#   999: 'FELIXF',        # remove
#   999: 'FELLERK',       # remove
#   999: 'FRANFOS',       # Frank Fosco
#   999: 'FRANKC',        # remove
#   999: 'FRANKCO',       # REMOVED
#   999: 'FRANKE',        # remove
#   999: 'FRANKF',        # remove
#   999: 'FRANKPAT',      # Frank Patino
#   999: 'FRASHOV',       # Frank Shover
#   999: 'FREDACRI',      # Fred Acri
#   999: 'FREDRAY',       # Fred Ray
#   999: 'FREDSM',        # Fred Smith
#   999: 'GARBIE',        # Gary Biederer
#   999: 'GARETTN',       # remove
#   999: 'GARYABEL',      # Gary Abelson
#   999: 'GARYROSS',      # remove
#   999: 'GARYSM',        # Gary Smith
#   999: 'GENEK',         # Gene Koch
#   999: 'GENES',         # remove
#   999: 'GENET',         # Gene Thomas
#   999: 'GEORGEFERN',    # George Fernandez
#   999: 'GEORGEP',       # remove
#   999: 'GEORGEPER',     # George Perkins
#   999: 'GEORGEU',       # remove
#   999: 'GEORGEW',       # remove
#   999: 'GERALDINEG',    # Remove
#   999: 'GERALDP',       # REMOVE
#   999: 'GERALDS',       # remove
#   999: 'GERIMCE',       # Remove
#   999: 'GINNYU',        # remove
#   999: 'GLADYSL',       # remove
#   999: 'GLENCO',        # Remove
#   999: 'GLENDAL',       # remove
#   999: 'GLENNG',        # Glenn Goodale
#   999: 'GLOELM',        # Gloria Elmore
#   999: 'GLORIANIC',     # remove
#   999: 'GUYC',          # REMOVE
#   999: 'GUYCHI',        # Guy Chidiac
#   999: 'GWENS',         # Remove
#   999: 'HARKAP',        # Harry Kaplan
#   999: 'HARSMI',        # Harry Smith
#   999: 'HARVEYL',       # Remove
#   999: 'HEINZK',        # remove
#   999: 'HELENACUS',     # Helena Cusumano
#   999: 'HELENBEAL',     # Remove
#   999: 'HENRYP',        # Removed
#   999: 'HERBA',         # remove
#   999: 'HERBROLFES',    # Herb Rolfes
#   999: 'HIRAML',        # remove
#   999: 'HOLMESS',       # remove
#   999: 'HOWSTE',        # Howard Stephenson
#   999: 'HYL',           # remove
#   999: 'ILENEW',        # remove
#   999: 'IRENEW',        # remove
#   999: 'IRISM',         # remove
#   999: 'JACKHOS',       # Jack Hoskins
#   999: 'JACKIETH',      # Jackie Thornhill
#   999: 'JACKSAW',       # Jack Sawatzki
#   999: 'JAMESB',        # remove
#   999: 'JAMESM',        # Remove
#   999: 'JANB',          # Remove
#   999: 'JANEC',         # remove
#   999: 'JANETM',        # Remove
#   999: 'JANETWOOL',     # Janet Wooley
#   999: 'JANFISC',       # Jan Fischer
#   999: 'JANHOH',        # removed
#   999: 'JANROUT',       # Janice Routh
#   999: 'JANSCH',        # Janis Schoen
#   999: 'JAYGO',         # Jay Goldenberg
#   999: 'JEANB',         # Remove
#   999: 'JEANNES',       # remove
#   999: 'JEANTAL',       # Jeannette Talarico
#   999: 'JEANW',         # remove
#   999: 'JEFFGR',        # Jeffrey Green
#   999: 'JERHOFF',       # Jerry Hoffspiegel
#   999: 'JERREW',        # Remove
#   999: 'JERRY NY',      # remove
#   999: 'JERRYFORD',     # Jerry Ford
#   999: 'JERRYJESOR',    # Remove
#   999: 'JERRYK',        # Remove
#   999: 'JERRYM',        # remove
#   999: 'JERRYS',        # remove
#   999: 'JERRYW',        # remove
#   999: 'JERRYWI',       # Remove
#   999: 'JERTAK',        # Jerry Takier
#   999: 'JIMCAR',        # Jim Carey
#   999: 'JIMEN',         # remove
#   999: 'JIMGAUG',       # remove
#   999: 'JIMK',          # remove
#   999: 'JIMKUEHL',      # remove
#   999: 'JIMPA',         # Remove
#   999: 'JIMS',          # Remove
#   999: 'JIMTHO',        # Jim Thompson
#   999: 'JOANBOW',       # Joan Bower
#   999: 'JOANKRANE',     # remove
#   999: 'JOANNER',       # Remove
#   999: 'JOANP',         # remove
#   999: 'JOANVOR',       # Joanne Vorhies
#   999: 'JOEASHE',       # removed
#   999: 'JOEC',          # Joe Connors
#   999: 'JOED',          # Remove
#   999: 'JOEOCON',       # Joe O'Connell
#   999: 'JOER',          # remove
#   999: 'JOET',          # remove see joseph
#   999: 'JOETUNK',       # Joe Tunkel
#   999: 'JOHNBARR',      # John Barrett
#   999: 'JOHNCONT',      # remove
#   999: 'JOHNCOOP',      # Remove
#   999: 'JOHNEB',        # remove
#   999: 'JOHNHOW',       # John Howland
#   999: 'JOHNMAR',       # removed
#   999: 'JOHNMC',        # Remove
#   999: 'JOHNNICH',      # remove
#   999: 'JOHNNOV',       # John Novicky
#   999: 'JOHNP',         # remove
#   999: 'JOHNR',         # remove
#   999: 'JOHNSNI',       # John Snipes
#   999: 'JOHNVO',        # John Vosicky
#   999: 'JONBRO',        # Jon Brown
#   999: 'JOSEPHW',       # remove
#   999: 'JOSETTEF',      # remove
#   999: 'JOSVAM',        # Joshua Vampan
#   999: 'JOYCEC',        # Remove
#   999: 'JRBAJ',         # JR Bajarias
#   999: 'JUDIEK',        # remove
#   999: 'JUDITHR',       # remove
#   999: 'JUDYG',         # Remove
#   999: 'JULIEF',        # Remove
#   999: 'JULKISO',       # Julie Kisosondi
#   999: 'JUNEP',         # remove
#   999: 'JUNWAN',        # Jun Wei Wang
#   999: 'KARENHEL',      # Karen Helander
#   999: 'KARENPET',      # Remove
#   999: 'KARENRICH',     # remove
#   999: 'KARWIL',        # Kari Wilburn
#   999: 'KASTROLLM',     # Remove
#   999: 'KATCLE',        # Kathleen Clemensen
#   999: 'KATHCOL',       # Kathy Colton
#   999: 'KATHDIS',       # Kathy Disabato
#   999: 'KATHIM',        # remove
#   999: 'KATHRYNW',      # Kathryn Wirth
#   999: 'KATHYLYONS',    # remove
#   999: 'KATLEE',        # Katherine Lee
#   999: 'KATVOS',        # Kathi Vosicky
#   999: 'KAYB',          # remove
#   999: 'KENM',          # remove
#   999: 'KENR',          # remove
#   999: 'KEVHAW',        # Kevin Hawley
#   999: 'KIMJEN',        # Kim Jensen
#   999: 'LARRYBAU',      # Remove
#   999: 'LARRYD',        # Remove
#   999: 'LARRYIRV',      # Larry Irvine
#   999: 'LARRYK',        # remove
#   999: 'LARWIL',        # Larry Williams
#   999: 'LAUMAK',        # Lauren Makar
#   999: 'LAURALOU',      # Remove
#   999: 'LAURIEH',       # remove
#   999: 'LAURIEHU',      # remove
#   999: 'LEIGHG',        # Remove
#   999: 'LEONARDH',      # removed
#   999: 'LINDAF',        # remove
#   999: 'LINDAFITZ',     # remove
#   999: 'LINDAL',        # removed
#   999: 'LINDAM',        # Remove
#   999: 'LINDAPA',       # Remove
#   999: 'LINDASWIT',     # Linda Switzer
#   999: 'LINNGU',        # Linda Nguyen
#   999: 'LINS',          # Remove
#   999: 'LITASA',        # Lita Sadorra
#   999: 'LIZDEV',        # Liz Devilbiss
#   999: 'LORETTAG',      # remove
#   999: 'LORETTASAB',    # Loretta Sabella
#   999: 'LOUFORT',       # remove
#   999: 'LOUISD',        # remove
#   999: 'LOUISECARR',    # Remove
#   999: 'LOUISPOL',      # remove
#   999: 'LWOLFE',        # Lynn Wolfe
#   999: 'LYNDACAR',      # remove
#   999: 'LYNNEB',        # Remove
#   999: 'LYNNWOLFE',     # Lynn Wolfe
#   999: 'MALK',          # remove
#   999: 'MANNYA',        # Remove
#   999: 'MARCOL',        # Margie Colyer
#   999: 'MARFRAN',       # Marcia Frank
#   999: 'MARGARETC',     # REMOVE
#   999: 'MARGEBR',       # remove
#   999: 'MARGIEA',       # Margie Abelson
#   999: 'MARIAMEL',      # Maria Melgarejo
#   999: 'MARIANDESUM',   # Marian De Sumrak
#   999: 'MARINELLB',     # Remove
#   999: 'MARKOR',        # Mark O'Rourke
#   999: 'MARKPY',        # Mark Pywell
#   999: 'MARKSTE',       # Mark Stevens
#   999: 'MARKWE',        # Mark West
#   999: 'MARLAG',        # Marla Lagattuta
#   999: 'MARSWIT',       # Mary Switzer
#   999: 'MARTHAG',       # Remove
#   999: 'MARTINJ',       # Remove
#   999: 'MARTINW',       # remove
#   999: 'MARWES',        # Mark West
#   999: 'MARYANNM',      # Mary Ann Massey
#   999: 'MARYBASHIST',   # Mary Bashist
#   999: 'MARYENG',       # Mary Engle
#   999: 'MARYF',         # remove
#   999: 'MARYJO',        # Mary Jo Brown
#   999: 'MARYJU',        # Mary Jane Ursem
#   999: 'MATTKIS',       # Matthew Kisosondi
#   999: 'MAUMCC',        # Maureen Mc Cartin
#   999: 'MAXR',          # remove
#   999: 'MAYTAH',        # May Tahmassebi
#   999: 'MELWISE',       # Melanie Wiseman
#   999: 'MICHAELT',      # remove
#   999: 'MICHBIRN',      # Michael Birnbaum
#   999: 'MICHELEVANT',   # Michele VanTassell
#   999: 'MIKEC',         # remove
#   999: 'MIKEFEFFER',    # remove
#   999: 'MIKEMAYNE',     # Mike Mayne
#   999: 'MIKGAL',        # Michael Galovits
#   999: 'MILESG',        # Remove
#   999: 'MILTBERK',      # Milton Berkowitz
#   999: 'MISPEC',        # Michael Speciale
#   999: 'MITCHC',        # Remove
#   999: 'MITSWE',        # Mitch Swetsky
#   999: 'MMASSEY',       # MaryAnn Massey
#   999: 'MOLLYSHER',     # Molly Sher
#   999: 'MORTO',         # remove
#   999: 'MURRAYW',       # remove
#   999: 'MYRONG',        # Remove
#   999: 'NADINEC',       # remove
#   999: 'NANCYKO',       # remove
#   999: 'NANCYLUCK',     # Nancy Lucke
#   999: 'NANCYM',        # remove
#   999: 'NANCYPOP',      # remove
#   999: 'NANHOSK',       # Nancy Hoskins
#   999: 'NAOMIS',        # remove
#   999: 'NEILB',         # remove
#   999: 'NICKIR',        # remove
#   999: 'NORLEYS',       # remove
#   999: 'NORMAL',        # remove
#   999: 'NORMD',         # remove
#   999: 'NORMR',         # remove
#   999: 'NORMW',         # remove
#   999: 'NYIRIJ',        # remove
#   999: 'PAIVOH',        # Paige Vorhies
#   999: 'PAMCON',        # Pam Conboy
#   999: 'PAMROSS',       # remove
#   999: 'PATB',          # remove
#   999: 'PATBR',         # remove
#   999: 'PATDAV',        # Patricia Davis
#   999: 'PATFAIV',       # Patrick Faivre
#   999: 'PATLEM',        # remove
#   999: 'PATSPE',        # Pat Spear
#   999: 'PATTIM',        # Patti Malczewski
#   999: 'PATWIL',        # Patty Wills
#   999: 'PAULAND',       # Paula Anderson
#   999: 'PAULANDER',     # Paul Andersen
#   999: 'PAULLUS',       # Paul Luszcz
#   999: 'PAULM',         # remove
#   999: 'PEDROH',        # remove
#   999: 'PEPINM',        # Pepin Meierhofer
#   999: 'PERCAN',        # Perry Cance
#   999: 'PERRYC',        # remove
#   999: 'PETEHAM',       # Remove
#   999: 'PETEO',         # Remove
#   999: 'PHIHON',        # Phil Horn
#   999: 'PRINE R',       # Remove
#   999: 'QTANAKA',       # remove
#   999: 'RALPHM',        # Remove
#   999: 'RANDYG',        # Randy Gast
#   999: 'RANZHANG',      # Ran Zhang
#   999: 'RAULGON',       # Raul Gonzalez
#   999: 'RAYC',          # remove
#   999: 'REXD',          # remove
#   999: 'RICHARDGILL',   # Remove
#   999: 'RICHARDRAN',    # remove
#   999: 'RICHARDWIL',    # Remove
#   999: 'RICHBEC',       # Richard Becker
#   999: 'RICHMOE',       # Richie Moeller
#   999: 'RICHVASQ',      # Richard Vasquez
#   999: 'RICHWEB',       # Richard Weber
#   999: 'RICLIN',        # Richard Linsmeier
#   999: 'RITAM',         # remove
#   999: 'ROBENG',        # Robert Engellenner
#   999: 'ROBERTH',       # remove
#   999: 'ROBERTR',       # Remove
#   999: 'ROBERTS',       # remove
#   999: 'ROBGREEN',      # Robert Greene
#   999: 'ROBINK',        # Remove
#   999: 'ROBINWOOL',     # Robin Wooley
#   999: 'ROBMAH',        # Robert Maher
#   999: 'ROGERB',        # Remove
#   999: 'ROGERS',        # remove
#   999: 'ROGERW',        # remove
#   999: 'ROGTOW',        # Roger Townsend
#   999: 'RONA',          # Remove
#   999: 'RONBROW',       # Ron Brow
#   999: 'RONMAIM',       # Ron Maimon
#   999: 'ROSABER',       # Roseanne Berkowitz
#   999: 'ROSEMARIEP',    # remove
#   999: 'ROSSR',         # remove
#   999: 'ROYBERG',       # Roy Berger
#   999: 'RUSSELLW',      # Remove
#   999: 'SANCOL',        # Sandy Collette
#   999: 'SANDICAR',      # remove
#   999: 'SANDYG',        # remove
#   999: 'SANDYV',        # Remove
#   999: 'SANKRAU',       # Sandra Krause
#   999: 'SARGRE',        # Sarah Greene
#   999: 'SCOTTIF',       # remove
#   999: 'SCOTTVEA',      # remove
#   999: 'SHARONABRA',    # remove
#   999: 'SHAVONHAN',     # Shavon Hankins
#   999: 'SHEKNA',        # Sheri Knaub
#   999: 'SHERCH',        # Sherli Chin
#   999: 'SHERLAS',       # Shirley Laster
#   999: 'SHIRLEET',      # remove
#   999: 'SHIRLEYBALL',   # remove
#   999: 'SHIRLEYDO',     # Remove
#   999: 'SHIRLTHOMP',    # Shirley Thompson
#   999: 'SIDO',          # remove
#   999: 'SILBAS',        # Silvia Basurto
#   999: 'SIMONH',        # remove
#   999: 'SOFCAST',       # Sofia Castille
#   999: 'STANB',         # remove
#   999: 'STANLEYR',      # remove
#   999: 'STANLEYW',      # removed
#   999: 'STEVEC',        # remove
#   999: 'STEVEHAN',      # Steve Handelman
#   999: 'STEVENIC',      # Steven Nicholas
#   999: 'STEVMEH',       # Steve Mehling
#   999: 'SUEEB',         # Remove
#   999: 'SUEGEFF',       # Remove
#   999: 'SUEP',          # remove
#   999: 'SUESCH',        # Sue Schniepp
#   999: 'SUESTEV',       # Remove
#   999: 'SUSANB',        # remove
#   999: 'SUSANEME',      # Susan Emerson
#   999: 'SUSANKIR',      # Susan Kirby
#   999: 'SUSANPOL',      # remove
#   999: 'SUSBRO',        # Susan Brown
#   999: 'SUSGAR',        # Susan Garcia
#   999: 'SUSYOU',        # Susan Young
#   999: 'TAIAKIN',       # Tai Akina
#   999: 'TEDDY',         # Ted Dyer
#   999: 'TEKASUM',       # Teka Summers
#   999: 'TERCAR',        # Terry Carey
#   999: 'TERESAF',       # remove
#   999: 'TERIV',         # remove
#   999: 'TERMATT',       # Terry Matter
#   999: 'TERRYMCM',      # remove
#   999: 'THERESEAND',    # Therese Andersen
#   999: 'TIBEASLEY',     # Ti Beasley
#   999: 'TIMK',          # remove
#   999: 'TIMLETO',       # Tim Letouzel
#   999: 'TOMB',          # Remove
#   999: 'TOMBURT',       # Tom Burt
#   999: 'TOMJENK',       # Tom Jenks
#   999: 'TOMK',          # Remove
#   999: 'TOMPOST',       # Thomas Post
#   999: 'TOMW',          # remove
#   999: 'TONIE',         # Remove
#   999: 'TONTOR',        # Tony Torres
#   999: 'TSUMEY',        # Tsuneko Meyers
#   999: 'VELMAL',        # Remove
#   999: 'VICKIEBAR',     # Vickie Baroch
#   999: 'VICKIMUST',     # remove
#   999: 'VICKYWALK',     # Vicky Walker
#   999: 'VINCENTM',      # remove
#   999: 'VINCENTP',      # remove
#   999: 'VINCES',        # remove
#   999: 'VINRICH',       # remove
#   999: 'VIRGILB',       # Remove
#   999: 'VLASTAB',       # Remove
#   999: 'WANDAK',        # remove
#   999: 'WILLG',         # remove
#   999: 'WORTHLYNN',     # Lynn Worthington


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

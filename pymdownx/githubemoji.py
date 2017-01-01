"""
Github Emoji.

pymdownx.githubemoji
Really simple plugin to add support for
github emojis

MIT license.

Copyright (c) 2014 - 2017 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from __future__ import unicode_literals
from markdown import Extension
from markdown.inlinepatterns import Pattern
from markdown import util
try:  # pragma: no cover
    import requests
    USE_REQUESTS = True
except Exception:  # pragma: no cover
    USE_REQUESTS = False
import json
import re
import copy
import warnings

RE_ASSET = re.compile(r'(?P<image>.*?/(?P<name>[^/]+?)\.png)(?:\?(?P<version>.+))?')

# --start--
RE_EMOJI = r'''(?x)
:(
    \+1|\-1|100|1234|1st\_place\_medal|2nd\_place\_medal|3rd\_place\_medal|8ball|a|ab|abc|abcd|accept
    |aerial\_tramway|afghanistan|airplane|aland\_islands|alarm\_clock|albania|alembic|algeria|alien|ambulance
    |american\_samoa|amphora|anchor|andorra|angel|anger|angola|angry|anguilla|anguished|ant|antarctica
    |antigua\_barbuda|apple|aquarius|argentina|aries|armenia|arrow\_backward|arrow\_double\_down|arrow\_double\_up
    |arrow\_down|arrow\_down\_small|arrow\_forward|arrow\_heading\_down|arrow\_heading\_up|arrow\_left
    |arrow\_lower\_left|arrow\_lower\_right|arrow\_right|arrow\_right\_hook|arrow\_up|arrow\_up\_down
    |arrow\_up\_small|arrow\_upper\_left|arrow\_upper\_right|arrows\_clockwise|arrows\_counterclockwise|art
    |articulated\_lorry|artificial\_satellite|aruba|asterisk|astonished|athletic\_shoe|atm|atom\_symbol|australia
    |austria|avocado|azerbaijan|b|baby|baby\_bottle|baby\_chick|baby\_symbol|back|bacon|badminton|baggage\_claim
    |baguette\_bread|bahamas|bahrain|balance\_scale|balloon|ballot\_box|ballot\_box\_with\_check|bamboo|banana
    |bangbang|bangladesh|bank|bar\_chart|barbados|barber|baseball|basecamp|basecampy|basketball|basketball\_man
    |basketball\_woman|bat|bath|bathtub|battery|beach\_umbrella|bear|bed|bee|beer|beers|beetle|beginner|belarus
    |belgium|belize|bell|bellhop\_bell|benin|bento|bermuda|bhutan|bicyclist|bike|biking\_man|biking\_woman|bikini
    |biohazard|bird|birthday|black\_circle|black\_flag|black\_heart|black\_joker|black\_large\_square
    |black\_medium\_small\_square|black\_medium\_square|black\_nib|black\_small\_square|black\_square\_button
    |blonde\_man|blonde\_woman|blossom|blowfish|blue\_book|blue\_car|blue\_heart|blush|boar|boat|bolivia|bomb|book
    |bookmark|bookmark\_tabs|books|boom|boot|bosnia\_herzegovina|botswana|bouquet|bow|bow\_and\_arrow|bowing\_man
    |bowing\_woman|bowling|bowtie|boxing\_glove|boy|brazil|bread|bride\_with\_veil|bridge\_at\_night|briefcase
    |british\_indian\_ocean\_territory|british\_virgin\_islands|broken\_heart|brunei|bug|building\_construction
    |bulb|bulgaria|bullettrain\_front|bullettrain\_side|burkina\_faso|burrito|burundi|bus
    |business\_suit\_levitating|busstop|bust\_in\_silhouette|busts\_in\_silhouette|butterfly|cactus|cake|calendar
    |call\_me\_hand|calling|cambodia|camel|camera|camera\_flash|cameroon|camping|canada|canary\_islands|cancer
    |candle|candy|canoe|cape\_verde|capital\_abcd|capricorn|car|card\_file\_box|card\_index|card\_index\_dividers
    |caribbean\_netherlands|carousel\_horse|carrot|cat|cat2|cayman\_islands|cd|central\_african\_republic|chad
    |chains|champagne|chart|chart\_with\_downwards\_trend|chart\_with\_upwards\_trend|checkered\_flag|cheese
    |cherries|cherry\_blossom|chestnut|chicken|children\_crossing|chile|chipmunk|chocolate\_bar|christmas\_island
    |christmas\_tree|church|cinema|circus\_tent|city\_sunrise|city\_sunset|cityscape|cl|clamp|clap|clapper
    |classical\_building|clinking\_glasses|clipboard|clock1|clock10|clock1030|clock11|clock1130|clock12|clock1230
    |clock130|clock2|clock230|clock3|clock330|clock4|clock430|clock5|clock530|clock6|clock630|clock7|clock730
    |clock8|clock830|clock9|clock930|closed\_book|closed\_lock\_with\_key|closed\_umbrella|cloud
    |cloud\_with\_lightning|cloud\_with\_lightning\_and\_rain|cloud\_with\_rain|cloud\_with\_snow|clown\_face
    |clubs|cn|cocktail|cocos\_islands|coffee|coffin|cold\_sweat|collision|colombia|comet|comoros|computer
    |computer\_mouse|confetti\_ball|confounded|confused|congo\_brazzaville|congo\_kinshasa|congratulations
    |construction|construction\_worker|construction\_worker\_man|construction\_worker\_woman|control\_knobs
    |convenience\_store|cook\_islands|cookie|cool|cop|copyright|corn|costa\_rica|cote\_divoire|couch\_and\_lamp
    |couple|couple\_with\_heart|couple\_with\_heart\_man\_man|couple\_with\_heart\_woman\_man
    |couple\_with\_heart\_woman\_woman|couplekiss\_man\_man|couplekiss\_man\_woman|couplekiss\_woman\_woman|cow
    |cow2|cowboy\_hat\_face|crab|crayon|credit\_card|crescent\_moon|cricket|croatia|crocodile|croissant
    |crossed\_fingers|crossed\_flags|crossed\_swords|crown|cry|crying\_cat\_face|crystal\_ball|cuba|cucumber|cupid
    |curacao|curly\_loop|currency\_exchange|curry|custard|customs|cyclone|cyprus|czech\_republic|dagger|dancer
    |dancers|dancing\_men|dancing\_women|dango|dark\_sunglasses|dart|dash|date|de|deciduous\_tree|deer|denmark
    |department\_store|derelict\_house|desert|desert\_island|desktop\_computer|detective
    |diamond\_shape\_with\_a\_dot\_inside|diamonds|disappointed|disappointed\_relieved|dizzy|dizzy\_face|djibouti
    |do\_not\_litter|dog|dog2|dollar|dolls|dolphin|dominica|dominican\_republic|door|doughnut|dove|dragon
    |dragon\_face|dress|dromedary\_camel|drooling\_face|droplet|drum|duck|dvd|e\-mail|eagle|ear|ear\_of\_rice
    |earth\_africa|earth\_americas|earth\_asia|ecuador|egg|eggplant|egypt|eight|eight\_pointed\_black\_star
    |eight\_spoked\_asterisk|el\_salvador|electric\_plug|elephant|email|end|envelope|envelope\_with\_arrow
    |equatorial\_guinea|eritrea|es|estonia|ethiopia|eu|euro|european\_castle|european\_post\_office
    |european\_union|evergreen\_tree|exclamation|expressionless|eye|eye\_speech\_bubble|eyeglasses|eyes
    |face\_with\_head\_bandage|face\_with\_thermometer|facepunch|factory|falkland\_islands|fallen\_leaf|family
    |family\_man\_boy|family\_man\_boy\_boy|family\_man\_girl|family\_man\_girl\_boy|family\_man\_girl\_girl
    |family\_man\_man\_boy|family\_man\_man\_boy\_boy|family\_man\_man\_girl|family\_man\_man\_girl\_boy
    |family\_man\_man\_girl\_girl|family\_man\_woman\_boy|family\_man\_woman\_boy\_boy|family\_man\_woman\_girl
    |family\_man\_woman\_girl\_boy|family\_man\_woman\_girl\_girl|family\_woman\_boy|family\_woman\_boy\_boy
    |family\_woman\_girl|family\_woman\_girl\_boy|family\_woman\_girl\_girl|family\_woman\_woman\_boy
    |family\_woman\_woman\_boy\_boy|family\_woman\_woman\_girl|family\_woman\_woman\_girl\_boy
    |family\_woman\_woman\_girl\_girl|faroe\_islands|fast\_forward|fax|fearful|feelsgood|feet|female\_detective
    |ferris\_wheel|ferry|field\_hockey|fiji|file\_cabinet|file\_folder|film\_projector|film\_strip|finland
    |finnadie|fire|fire\_engine|fireworks|first\_quarter\_moon|first\_quarter\_moon\_with\_face|fish|fish\_cake
    |fishing\_pole\_and\_fish|fist|fist\_left|fist\_oncoming|fist\_raised|fist\_right|five|flags|flashlight
    |fleur\_de\_lis|flight\_arrival|flight\_departure|flipper|floppy\_disk|flower\_playing\_cards|flushed|fog
    |foggy|football|footprints|fork\_and\_knife|fountain|fountain\_pen|four|four\_leaf\_clover|fox\_face|fr
    |framed\_picture|free|french\_guiana|french\_polynesia|french\_southern\_territories|fried\_egg|fried\_shrimp
    |fries|frog|frowning|frowning\_face|frowning\_man|frowning\_woman|fu|fuelpump|full\_moon
    |full\_moon\_with\_face|funeral\_urn|gabon|gambia|game\_die|gb|gear|gem|gemini|georgia|ghana|ghost|gibraltar
    |gift|gift\_heart|girl|globe\_with\_meridians|goal\_net|goat|goberserk|godmode|golf|golfing\_man
    |golfing\_woman|gorilla|grapes|greece|green\_apple|green\_book|green\_heart|green\_salad|greenland|grenada
    |grey\_exclamation|grey\_question|grimacing|grin|grinning|guadeloupe|guam|guardsman|guardswoman|guatemala
    |guernsey|guinea|guinea\_bissau|guitar|gun|guyana|haircut|haircut\_man|haircut\_woman|haiti|hamburger|hammer
    |hammer\_and\_pick|hammer\_and\_wrench|hamster|hand|handbag|handshake|hankey|hash|hatched\_chick
    |hatching\_chick|headphones|hear\_no\_evil|heart|heart\_decoration|heart\_eyes|heart\_eyes\_cat|heartbeat
    |heartpulse|hearts|heavy\_check\_mark|heavy\_division\_sign|heavy\_dollar\_sign|heavy\_exclamation\_mark
    |heavy\_heart\_exclamation|heavy\_minus\_sign|heavy\_multiplication\_x|heavy\_plus\_sign|helicopter|herb
    |hibiscus|high\_brightness|high\_heel|hocho|hole|honduras|honey\_pot|honeybee|hong\_kong|horse|horse\_racing
    |hospital|hot\_pepper|hotdog|hotel|hotsprings|hourglass|hourglass\_flowing\_sand|house|house\_with\_garden
    |houses|hugs|hungary|hurtrealbad|hushed|ice\_cream|ice\_hockey|ice\_skate|icecream|iceland|id
    |ideograph\_advantage|imp|inbox\_tray|incoming\_envelope|india|indonesia|information\_desk\_person
    |information\_source|innocent|interrobang|iphone|iran|iraq|ireland|isle\_of\_man|israel|it|izakaya\_lantern
    |jack\_o\_lantern|jamaica|japan|japanese\_castle|japanese\_goblin|japanese\_ogre|jeans|jersey|jordan|joy
    |joy\_cat|joystick|jp|kaaba|kazakhstan|kenya|key|keyboard|keycap\_ten|kick\_scooter|kimono|kiribati|kiss
    |kissing|kissing\_cat|kissing\_closed\_eyes|kissing\_heart|kissing\_smiling\_eyes|kiwi\_fruit|knife|koala|koko
    |kosovo|kr|kuwait|kyrgyzstan|label|lantern|laos|large\_blue\_circle|large\_blue\_diamond
    |large\_orange\_diamond|last\_quarter\_moon|last\_quarter\_moon\_with\_face|latin\_cross|latvia|laughing
    |leaves|lebanon|ledger|left\_luggage|left\_right\_arrow|leftwards\_arrow\_with\_hook|lemon|leo|leopard|lesotho
    |level\_slider|liberia|libra|libya|liechtenstein|light\_rail|link|lion|lips|lipstick|lithuania|lizard|lock
    |lock\_with\_ink\_pen|lollipop|loop|loud\_sound|loudspeaker|love\_hotel|love\_letter|low\_brightness
    |luxembourg|lying\_face|m|macau|macedonia|madagascar|mag|mag\_right|mahjong|mailbox|mailbox\_closed
    |mailbox\_with\_mail|mailbox\_with\_no\_mail|malawi|malaysia|maldives|male\_detective|mali|malta|man
    |man\_artist|man\_astronaut|man\_cartwheeling|man\_cook|man\_dancing|man\_facepalming|man\_factory\_worker
    |man\_farmer|man\_firefighter|man\_health\_worker|man\_in\_tuxedo|man\_judge|man\_juggling|man\_mechanic
    |man\_office\_worker|man\_pilot|man\_playing\_handball|man\_playing\_water\_polo|man\_scientist|man\_shrugging
    |man\_singer|man\_student|man\_teacher|man\_technologist|man\_with\_gua\_pi\_mao|man\_with\_turban|mandarin
    |mans\_shoe|mantelpiece\_clock|maple\_leaf|marshall\_islands|martial\_arts\_uniform|martinique|mask|massage
    |massage\_man|massage\_woman|mauritania|mauritius|mayotte|meat\_on\_bone|medal\_military|medal\_sports|mega
    |melon|memo|men\_wrestling|menorah|mens|metal|metro|mexico|micronesia|microphone|microscope|middle\_finger
    |milk\_glass|milky\_way|minibus|minidisc|mobile\_phone\_off|moldova|monaco|money\_mouth\_face
    |money\_with\_wings|moneybag|mongolia|monkey|monkey\_face|monorail|montenegro|montserrat|moon|morocco
    |mortar\_board|mosque|motor\_boat|motor\_scooter|motorcycle|motorway|mount\_fuji|mountain|mountain\_bicyclist
    |mountain\_biking\_man|mountain\_biking\_woman|mountain\_cableway|mountain\_railway|mountain\_snow|mouse
    |mouse2|movie\_camera|moyai|mozambique|mrs\_claus|muscle|mushroom|musical\_keyboard|musical\_note
    |musical\_score|mute|myanmar|nail\_care|name\_badge|namibia|national\_park|nauru|nauseated\_face|neckbeard
    |necktie|negative\_squared\_cross\_mark|nepal|nerd\_face|netherlands|neutral\_face|new|new\_caledonia
    |new\_moon|new\_moon\_with\_face|new\_zealand|newspaper|newspaper\_roll|next\_track\_button|ng|ng\_man
    |ng\_woman|nicaragua|niger|nigeria|night\_with\_stars|nine|niue|no\_bell|no\_bicycles|no\_entry
    |no\_entry\_sign|no\_good|no\_good\_man|no\_good\_woman|no\_mobile\_phones|no\_mouth|no\_pedestrians
    |no\_smoking|non\-potable\_water|norfolk\_island|north\_korea|northern\_mariana\_islands|norway|nose|notebook
    |notebook\_with\_decorative\_cover|notes|nut\_and\_bolt|o|o2|ocean|octocat|octopus|oden|office|oil\_drum|ok
    |ok\_hand|ok\_man|ok\_woman|old\_key|older\_man|older\_woman|om|oman|on|oncoming\_automobile|oncoming\_bus
    |oncoming\_police\_car|oncoming\_taxi|one|open\_book|open\_file\_folder|open\_hands|open\_mouth|open\_umbrella
    |ophiuchus|orange|orange\_book|orthodox\_cross|outbox\_tray|owl|ox|package|page\_facing\_up|page\_with\_curl
    |pager|paintbrush|pakistan|palau|palestinian\_territories|palm\_tree|panama|pancakes|panda\_face|paperclip
    |paperclips|papua\_new\_guinea|paraguay|parasol\_on\_ground|parking|part\_alternation\_mark|partly\_sunny
    |passenger\_ship|passport\_control|pause\_button|paw\_prints|peace\_symbol|peach|peanuts|pear|pen|pencil
    |pencil2|penguin|pensive|performing\_arts|persevere|person\_fencing|person\_frowning|person\_with\_blond\_hair
    |person\_with\_pouting\_face|peru|philippines|phone|pick|pig|pig2|pig\_nose|pill|pineapple|ping\_pong|pisces
    |pitcairn\_islands|pizza|place\_of\_worship|plate\_with\_cutlery|play\_or\_pause\_button|point\_down
    |point\_left|point\_right|point\_up|point\_up\_2|poland|police\_car|policeman|policewoman|poodle|poop|popcorn
    |portugal|post\_office|postal\_horn|postbox|potable\_water|potato|pouch|poultry\_leg|pound|pout|pouting\_cat
    |pouting\_man|pouting\_woman|pray|prayer\_beads|pregnant\_woman|previous\_track\_button|prince|princess
    |printer|puerto\_rico|punch|purple\_heart|purse|pushpin|put\_litter\_in\_its\_place|qatar|question|rabbit
    |rabbit2|racehorse|racing\_car|radio|radio\_button|radioactive|rage|rage1|rage2|rage3|rage4|railway\_car
    |railway\_track|rainbow|rainbow\_flag|raised\_back\_of\_hand|raised\_hand|raised\_hand\_with\_fingers\_splayed
    |raised\_hands|raising\_hand|raising\_hand\_man|raising\_hand\_woman|ram|ramen|rat|record\_button|recycle
    |red\_car|red\_circle|registered|relaxed|relieved|reminder\_ribbon|repeat|repeat\_one|rescue\_worker\_helmet
    |restroom|reunion|revolving\_hearts|rewind|rhinoceros|ribbon|rice|rice\_ball|rice\_cracker|rice\_scene
    |right\_anger\_bubble|ring|robot|rocket|rofl|roll\_eyes|roller\_coaster|romania|rooster|rose|rosette
    |rotating\_light|round\_pushpin|rowboat|rowing\_man|rowing\_woman|ru|rugby\_football|runner|running
    |running\_man|running\_shirt\_with\_sash|running\_woman|rwanda|sa|sagittarius|sailboat|sake|samoa|san\_marino
    |sandal|santa|sao\_tome\_principe|satellite|satisfied|saudi\_arabia|saxophone|school|school\_satchel|scissors
    |scorpion|scorpius|scream|scream\_cat|scroll|seat|secret|see\_no\_evil|seedling|selfie|senegal|serbia|seven
    |seychelles|shallow\_pan\_of\_food|shamrock|shark|shaved\_ice|sheep|shell|shield|shinto\_shrine|ship|shipit
    |shirt|shit|shoe|shopping|shopping\_cart|shower|shrimp|sierra\_leone|signal\_strength|singapore|sint\_maarten
    |six|six\_pointed\_star|ski|skier|skull|skull\_and\_crossbones|sleeping|sleeping\_bed|sleepy
    |slightly\_frowning\_face|slightly\_smiling\_face|slot\_machine|slovakia|slovenia|small\_airplane
    |small\_blue\_diamond|small\_orange\_diamond|small\_red\_triangle|small\_red\_triangle\_down|smile|smile\_cat
    |smiley|smiley\_cat|smiling\_imp|smirk|smirk\_cat|smoking|snail|snake|sneezing\_face|snowboarder|snowflake
    |snowman|snowman\_with\_snow|sob|soccer|solomon\_islands|somalia|soon|sos|sound|south\_africa
    |south\_georgia\_south\_sandwich\_islands|south\_sudan|space\_invader|spades|spaghetti|sparkle|sparkler
    |sparkles|sparkling\_heart|speak\_no\_evil|speaker|speaking\_head|speech\_balloon|speedboat|spider|spider\_web
    |spiral\_calendar|spiral\_notepad|spoon|squid|squirrel|sri\_lanka|st\_barthelemy|st\_helena|st\_kitts\_nevis
    |st\_lucia|st\_pierre\_miquelon|st\_vincent\_grenadines|stadium|star|star2|star\_and\_crescent|star\_of\_david
    |stars|station|statue\_of\_liberty|steam\_locomotive|stew|stop\_button|stop\_sign|stopwatch|straight\_ruler
    |strawberry|stuck\_out\_tongue|stuck\_out\_tongue\_closed\_eyes|stuck\_out\_tongue\_winking\_eye
    |studio\_microphone|stuffed\_flatbread|sudan|sun\_behind\_large\_cloud|sun\_behind\_rain\_cloud
    |sun\_behind\_small\_cloud|sun\_with\_face|sunflower|sunglasses|sunny|sunrise|sunrise\_over\_mountains|surfer
    |surfing\_man|surfing\_woman|suriname|sushi|suspect|suspension\_railway|swaziland|sweat|sweat\_drops
    |sweat\_smile|sweden|sweet\_potato|swimmer|swimming\_man|swimming\_woman|switzerland|symbols|synagogue|syria
    |syringe|taco|tada|taiwan|tajikistan|tanabata\_tree|tangerine|tanzania|taurus|taxi|tea|telephone
    |telephone\_receiver|telescope|tennis|tent|thailand|thermometer|thinking|thought\_balloon|three|thumbsdown
    |thumbsup|ticket|tickets|tiger|tiger2|timer\_clock|timor\_leste|tipping\_hand\_man|tipping\_hand\_woman
    |tired\_face|tm|togo|toilet|tokelau|tokyo\_tower|tomato|tonga|tongue|top|tophat|tornado|tr|trackball|tractor
    |traffic\_light|train|train2|tram|triangular\_flag\_on\_post|triangular\_ruler|trident|trinidad\_tobago
    |triumph|trolleybus|trollface|trophy|tropical\_drink|tropical\_fish|truck|trumpet|tshirt|tulip|tumbler\_glass
    |tunisia|turkey|turkmenistan|turks\_caicos\_islands|turtle|tuvalu|tv|twisted\_rightwards\_arrows|two
    |two\_hearts|two\_men\_holding\_hands|two\_women\_holding\_hands|u5272|u5408|u55b6|u6307|u6708|u6709|u6e80
    |u7121|u7533|u7981|u7a7a|uganda|uk|ukraine|umbrella|unamused|underage|unicorn|united\_arab\_emirates|unlock|up
    |upside\_down\_face|uruguay|us|us\_virgin\_islands|uzbekistan|v|vanuatu|vatican\_city|venezuela
    |vertical\_traffic\_light|vhs|vibration\_mode|video\_camera|video\_game|vietnam|violin|virgo|volcano
    |volleyball|vs|vulcan\_salute|walking|walking\_man|walking\_woman|wallis\_futuna|waning\_crescent\_moon
    |waning\_gibbous\_moon|warning|wastebasket|watch|water\_buffalo|watermelon|wave|wavy\_dash
    |waxing\_crescent\_moon|waxing\_gibbous\_moon|wc|weary|wedding|weight\_lifting\_man|weight\_lifting\_woman
    |western\_sahara|whale|whale2|wheel\_of\_dharma|wheelchair|white\_check\_mark|white\_circle|white\_flag
    |white\_flower|white\_large\_square|white\_medium\_small\_square|white\_medium\_square|white\_small\_square
    |white\_square\_button|wilted\_flower|wind\_chime|wind\_face|wine\_glass|wink|wolf|woman|woman\_artist
    |woman\_astronaut|woman\_cartwheeling|woman\_cook|woman\_facepalming|woman\_factory\_worker|woman\_farmer
    |woman\_firefighter|woman\_health\_worker|woman\_judge|woman\_juggling|woman\_mechanic|woman\_office\_worker
    |woman\_pilot|woman\_playing\_handball|woman\_playing\_water\_polo|woman\_scientist|woman\_shrugging
    |woman\_singer|woman\_student|woman\_teacher|woman\_technologist|woman\_with\_turban|womans\_clothes
    |womans\_hat|women\_wrestling|womens|world\_map|worried|wrench|writing\_hand|x|yellow\_heart|yemen|yen
    |yin\_yang|yum|zambia|zap|zero|zimbabwe|zipper\_mouth\_face|zzz
):'''

URL_EMOJI = {
    "+1": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f44d.png",
    "-1": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f44e.png",
    "100": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4af.png",
    "1234": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f522.png",
    "1st_place_medal": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f947.png",
    "2nd_place_medal": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f948.png",
    "3rd_place_medal": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f949.png",
    "8ball": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3b1.png",
    "a": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f170.png",
    "ab": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f18e.png",
    "abc": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f524.png",
    "abcd": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f521.png",
    "accept": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f251.png",
    "aerial_tramway": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6a1.png",
    "afghanistan": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e6-1f1eb.png",
    "airplane": "https://assets-cdn.github.com/images/icons/emoji/unicode/2708.png",
    "aland_islands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e6-1f1fd.png",
    "alarm_clock": "https://assets-cdn.github.com/images/icons/emoji/unicode/23f0.png",
    "albania": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e6-1f1f1.png",
    "alembic": "https://assets-cdn.github.com/images/icons/emoji/unicode/2697.png",
    "algeria": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e9-1f1ff.png",
    "alien": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f47d.png",
    "ambulance": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f691.png",
    "american_samoa": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e6-1f1f8.png",
    "amphora": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3fa.png",
    "anchor": "https://assets-cdn.github.com/images/icons/emoji/unicode/2693.png",
    "andorra": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e6-1f1e9.png",
    "angel": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f47c.png",
    "anger": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4a2.png",
    "angola": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e6-1f1f4.png",
    "angry": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f620.png",
    "anguilla": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e6-1f1ee.png",
    "anguished": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f627.png",
    "ant": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f41c.png",
    "antarctica": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e6-1f1f6.png",
    "antigua_barbuda": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e6-1f1ec.png",
    "apple": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f34e.png",
    "aquarius": "https://assets-cdn.github.com/images/icons/emoji/unicode/2652.png",
    "argentina": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e6-1f1f7.png",
    "aries": "https://assets-cdn.github.com/images/icons/emoji/unicode/2648.png",
    "armenia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e6-1f1f2.png",
    "arrow_backward": "https://assets-cdn.github.com/images/icons/emoji/unicode/25c0.png",
    "arrow_double_down": "https://assets-cdn.github.com/images/icons/emoji/unicode/23ec.png",
    "arrow_double_up": "https://assets-cdn.github.com/images/icons/emoji/unicode/23eb.png",
    "arrow_down": "https://assets-cdn.github.com/images/icons/emoji/unicode/2b07.png",
    "arrow_down_small": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f53d.png",
    "arrow_forward": "https://assets-cdn.github.com/images/icons/emoji/unicode/25b6.png",
    "arrow_heading_down": "https://assets-cdn.github.com/images/icons/emoji/unicode/2935.png",
    "arrow_heading_up": "https://assets-cdn.github.com/images/icons/emoji/unicode/2934.png",
    "arrow_left": "https://assets-cdn.github.com/images/icons/emoji/unicode/2b05.png",
    "arrow_lower_left": "https://assets-cdn.github.com/images/icons/emoji/unicode/2199.png",
    "arrow_lower_right": "https://assets-cdn.github.com/images/icons/emoji/unicode/2198.png",
    "arrow_right": "https://assets-cdn.github.com/images/icons/emoji/unicode/27a1.png",
    "arrow_right_hook": "https://assets-cdn.github.com/images/icons/emoji/unicode/21aa.png",
    "arrow_up": "https://assets-cdn.github.com/images/icons/emoji/unicode/2b06.png",
    "arrow_up_down": "https://assets-cdn.github.com/images/icons/emoji/unicode/2195.png",
    "arrow_up_small": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f53c.png",
    "arrow_upper_left": "https://assets-cdn.github.com/images/icons/emoji/unicode/2196.png",
    "arrow_upper_right": "https://assets-cdn.github.com/images/icons/emoji/unicode/2197.png",
    "arrows_clockwise": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f503.png",
    "arrows_counterclockwise": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f504.png",
    "art": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3a8.png",
    "articulated_lorry": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f69b.png",
    "artificial_satellite": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6f0.png",
    "aruba": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e6-1f1fc.png",
    "asterisk": "https://assets-cdn.github.com/images/icons/emoji/unicode/002a-20e3.png",
    "astonished": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f632.png",
    "athletic_shoe": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f45f.png",
    "atm": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3e7.png",
    "atom_symbol": "https://assets-cdn.github.com/images/icons/emoji/unicode/269b.png",
    "australia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e6-1f1fa.png",
    "austria": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e6-1f1f9.png",
    "avocado": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f951.png",
    "azerbaijan": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e6-1f1ff.png",
    "b": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f171.png",
    "baby": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f476.png",
    "baby_bottle": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f37c.png",
    "baby_chick": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f424.png",
    "baby_symbol": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6bc.png",
    "back": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f519.png",
    "bacon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f953.png",
    "badminton": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3f8.png",
    "baggage_claim": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6c4.png",
    "baguette_bread": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f956.png",
    "bahamas": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e7-1f1f8.png",
    "bahrain": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e7-1f1ed.png",
    "balance_scale": "https://assets-cdn.github.com/images/icons/emoji/unicode/2696.png",
    "balloon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f388.png",
    "ballot_box": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5f3.png",
    "ballot_box_with_check": "https://assets-cdn.github.com/images/icons/emoji/unicode/2611.png",
    "bamboo": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f38d.png",
    "banana": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f34c.png",
    "bangbang": "https://assets-cdn.github.com/images/icons/emoji/unicode/203c.png",
    "bangladesh": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e7-1f1e9.png",
    "bank": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3e6.png",
    "bar_chart": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4ca.png",
    "barbados": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e7-1f1e7.png",
    "barber": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f488.png",
    "baseball": "https://assets-cdn.github.com/images/icons/emoji/unicode/26be.png",
    "basecamp": "https://assets-cdn.github.com/images/icons/emoji/basecamp.png",
    "basecampy": "https://assets-cdn.github.com/images/icons/emoji/basecampy.png",
    "basketball": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3c0.png",
    "basketball_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/26f9.png",
    "basketball_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/26f9-2640.png",
    "bat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f987.png",
    "bath": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6c0.png",
    "bathtub": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6c1.png",
    "battery": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f50b.png",
    "beach_umbrella": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3d6.png",
    "bear": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f43b.png",
    "bed": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6cf.png",
    "bee": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f41d.png",
    "beer": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f37a.png",
    "beers": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f37b.png",
    "beetle": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f41e.png",
    "beginner": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f530.png",
    "belarus": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e7-1f1fe.png",
    "belgium": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e7-1f1ea.png",
    "belize": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e7-1f1ff.png",
    "bell": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f514.png",
    "bellhop_bell": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6ce.png",
    "benin": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e7-1f1ef.png",
    "bento": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f371.png",
    "bermuda": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e7-1f1f2.png",
    "bhutan": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e7-1f1f9.png",
    "bicyclist": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6b4.png",
    "bike": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6b2.png",
    "biking_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6b4.png",
    "biking_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6b4-2640.png",
    "bikini": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f459.png",
    "biohazard": "https://assets-cdn.github.com/images/icons/emoji/unicode/2623.png",
    "bird": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f426.png",
    "birthday": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f382.png",
    "black_circle": "https://assets-cdn.github.com/images/icons/emoji/unicode/26ab.png",
    "black_flag": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3f4.png",
    "black_heart": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5a4.png",
    "black_joker": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f0cf.png",
    "black_large_square": "https://assets-cdn.github.com/images/icons/emoji/unicode/2b1b.png",
    "black_medium_small_square": "https://assets-cdn.github.com/images/icons/emoji/unicode/25fe.png",
    "black_medium_square": "https://assets-cdn.github.com/images/icons/emoji/unicode/25fc.png",
    "black_nib": "https://assets-cdn.github.com/images/icons/emoji/unicode/2712.png",
    "black_small_square": "https://assets-cdn.github.com/images/icons/emoji/unicode/25aa.png",
    "black_square_button": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f532.png",
    "blonde_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f471.png",
    "blonde_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f471-2640.png",
    "blossom": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f33c.png",
    "blowfish": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f421.png",
    "blue_book": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4d8.png",
    "blue_car": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f699.png",
    "blue_heart": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f499.png",
    "blush": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f60a.png",
    "boar": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f417.png",
    "boat": "https://assets-cdn.github.com/images/icons/emoji/unicode/26f5.png",
    "bolivia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e7-1f1f4.png",
    "bomb": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4a3.png",
    "book": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4d6.png",
    "bookmark": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f516.png",
    "bookmark_tabs": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4d1.png",
    "books": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4da.png",
    "boom": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4a5.png",
    "boot": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f462.png",
    "bosnia_herzegovina": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e7-1f1e6.png",
    "botswana": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e7-1f1fc.png",
    "bouquet": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f490.png",
    "bow": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f647.png",
    "bow_and_arrow": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3f9.png",
    "bowing_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f647.png",
    "bowing_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f647-2640.png",
    "bowling": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3b3.png",
    "bowtie": "https://assets-cdn.github.com/images/icons/emoji/bowtie.png",
    "boxing_glove": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f94a.png",
    "boy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f466.png",
    "brazil": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e7-1f1f7.png",
    "bread": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f35e.png",
    "bride_with_veil": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f470.png",
    "bridge_at_night": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f309.png",
    "briefcase": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4bc.png",
    "british_indian_ocean_territory": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ee-1f1f4.png",
    "british_virgin_islands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1fb-1f1ec.png",
    "broken_heart": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f494.png",
    "brunei": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e7-1f1f3.png",
    "bug": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f41b.png",
    "building_construction": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3d7.png",
    "bulb": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4a1.png",
    "bulgaria": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e7-1f1ec.png",
    "bullettrain_front": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f685.png",
    "bullettrain_side": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f684.png",
    "burkina_faso": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e7-1f1eb.png",
    "burrito": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f32f.png",
    "burundi": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e7-1f1ee.png",
    "bus": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f68c.png",
    "business_suit_levitating": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f574.png",
    "busstop": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f68f.png",
    "bust_in_silhouette": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f464.png",
    "busts_in_silhouette": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f465.png",
    "butterfly": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f98b.png",
    "cactus": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f335.png",
    "cake": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f370.png",
    "calendar": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4c6.png",
    "call_me_hand": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f919.png",
    "calling": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4f2.png",
    "cambodia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f0-1f1ed.png",
    "camel": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f42b.png",
    "camera": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4f7.png",
    "camera_flash": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4f8.png",
    "cameroon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e8-1f1f2.png",
    "camping": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3d5.png",
    "canada": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e8-1f1e6.png",
    "canary_islands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ee-1f1e8.png",
    "cancer": "https://assets-cdn.github.com/images/icons/emoji/unicode/264b.png",
    "candle": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f56f.png",
    "candy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f36c.png",
    "canoe": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6f6.png",
    "cape_verde": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e8-1f1fb.png",
    "capital_abcd": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f520.png",
    "capricorn": "https://assets-cdn.github.com/images/icons/emoji/unicode/2651.png",
    "car": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f697.png",
    "card_file_box": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5c3.png",
    "card_index": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4c7.png",
    "card_index_dividers": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5c2.png",
    "caribbean_netherlands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e7-1f1f6.png",
    "carousel_horse": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3a0.png",
    "carrot": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f955.png",
    "cat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f431.png",
    "cat2": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f408.png",
    "cayman_islands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f0-1f1fe.png",
    "cd": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4bf.png",
    "central_african_republic": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e8-1f1eb.png",
    "chad": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f9-1f1e9.png",
    "chains": "https://assets-cdn.github.com/images/icons/emoji/unicode/26d3.png",
    "champagne": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f37e.png",
    "chart": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4b9.png",
    "chart_with_downwards_trend": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4c9.png",
    "chart_with_upwards_trend": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4c8.png",
    "checkered_flag": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3c1.png",
    "cheese": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f9c0.png",
    "cherries": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f352.png",
    "cherry_blossom": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f338.png",
    "chestnut": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f330.png",
    "chicken": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f414.png",
    "children_crossing": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6b8.png",
    "chile": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e8-1f1f1.png",
    "chipmunk": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f43f.png",
    "chocolate_bar": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f36b.png",
    "christmas_island": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e8-1f1fd.png",
    "christmas_tree": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f384.png",
    "church": "https://assets-cdn.github.com/images/icons/emoji/unicode/26ea.png",
    "cinema": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3a6.png",
    "circus_tent": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3aa.png",
    "city_sunrise": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f307.png",
    "city_sunset": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f306.png",
    "cityscape": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3d9.png",
    "cl": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f191.png",
    "clamp": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5dc.png",
    "clap": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f44f.png",
    "clapper": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3ac.png",
    "classical_building": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3db.png",
    "clinking_glasses": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f942.png",
    "clipboard": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4cb.png",
    "clock1": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f550.png",
    "clock10": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f559.png",
    "clock1030": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f565.png",
    "clock11": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f55a.png",
    "clock1130": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f566.png",
    "clock12": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f55b.png",
    "clock1230": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f567.png",
    "clock130": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f55c.png",
    "clock2": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f551.png",
    "clock230": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f55d.png",
    "clock3": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f552.png",
    "clock330": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f55e.png",
    "clock4": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f553.png",
    "clock430": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f55f.png",
    "clock5": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f554.png",
    "clock530": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f560.png",
    "clock6": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f555.png",
    "clock630": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f561.png",
    "clock7": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f556.png",
    "clock730": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f562.png",
    "clock8": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f557.png",
    "clock830": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f563.png",
    "clock9": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f558.png",
    "clock930": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f564.png",
    "closed_book": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4d5.png",
    "closed_lock_with_key": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f510.png",
    "closed_umbrella": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f302.png",
    "cloud": "https://assets-cdn.github.com/images/icons/emoji/unicode/2601.png",
    "cloud_with_lightning": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f329.png",
    "cloud_with_lightning_and_rain": "https://assets-cdn.github.com/images/icons/emoji/unicode/26c8.png",
    "cloud_with_rain": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f327.png",
    "cloud_with_snow": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f328.png",
    "clown_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f921.png",
    "clubs": "https://assets-cdn.github.com/images/icons/emoji/unicode/2663.png",
    "cn": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e8-1f1f3.png",
    "cocktail": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f378.png",
    "cocos_islands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e8-1f1e8.png",
    "coffee": "https://assets-cdn.github.com/images/icons/emoji/unicode/2615.png",
    "coffin": "https://assets-cdn.github.com/images/icons/emoji/unicode/26b0.png",
    "cold_sweat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f630.png",
    "collision": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4a5.png",
    "colombia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e8-1f1f4.png",
    "comet": "https://assets-cdn.github.com/images/icons/emoji/unicode/2604.png",
    "comoros": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f0-1f1f2.png",
    "computer": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4bb.png",
    "computer_mouse": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5b1.png",
    "confetti_ball": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f38a.png",
    "confounded": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f616.png",
    "confused": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f615.png",
    "congo_brazzaville": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e8-1f1ec.png",
    "congo_kinshasa": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e8-1f1e9.png",
    "congratulations": "https://assets-cdn.github.com/images/icons/emoji/unicode/3297.png",
    "construction": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6a7.png",
    "construction_worker": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f477.png",
    "construction_worker_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f477.png",
    "construction_worker_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f477-2640.png",
    "control_knobs": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f39b.png",
    "convenience_store": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3ea.png",
    "cook_islands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e8-1f1f0.png",
    "cookie": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f36a.png",
    "cool": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f192.png",
    "cop": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f46e.png",
    "copyright": "https://assets-cdn.github.com/images/icons/emoji/unicode/00a9.png",
    "corn": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f33d.png",
    "costa_rica": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e8-1f1f7.png",
    "cote_divoire": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e8-1f1ee.png",
    "couch_and_lamp": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6cb.png",
    "couple": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f46b.png",
    "couple_with_heart": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f491.png",
    "couple_with_heart_man_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-2764-1f468.png",
    "couple_with_heart_woman_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f491.png",
    "couple_with_heart_woman_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-2764-1f469.png",
    "couplekiss_man_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-2764-1f48b-1f468.png",
    "couplekiss_man_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f48f.png",
    "couplekiss_woman_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-2764-1f48b-1f469.png",
    "cow": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f42e.png",
    "cow2": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f404.png",
    "cowboy_hat_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f920.png",
    "crab": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f980.png",
    "crayon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f58d.png",
    "credit_card": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4b3.png",
    "crescent_moon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f319.png",
    "cricket": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3cf.png",
    "croatia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ed-1f1f7.png",
    "crocodile": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f40a.png",
    "croissant": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f950.png",
    "crossed_fingers": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f91e.png",
    "crossed_flags": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f38c.png",
    "crossed_swords": "https://assets-cdn.github.com/images/icons/emoji/unicode/2694.png",
    "crown": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f451.png",
    "cry": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f622.png",
    "crying_cat_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f63f.png",
    "crystal_ball": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f52e.png",
    "cuba": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e8-1f1fa.png",
    "cucumber": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f952.png",
    "cupid": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f498.png",
    "curacao": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e8-1f1fc.png",
    "curly_loop": "https://assets-cdn.github.com/images/icons/emoji/unicode/27b0.png",
    "currency_exchange": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4b1.png",
    "curry": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f35b.png",
    "custard": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f36e.png",
    "customs": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6c3.png",
    "cyclone": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f300.png",
    "cyprus": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e8-1f1fe.png",
    "czech_republic": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e8-1f1ff.png",
    "dagger": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5e1.png",
    "dancer": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f483.png",
    "dancers": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f46f.png",
    "dancing_men": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f46f-2642.png",
    "dancing_women": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f46f.png",
    "dango": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f361.png",
    "dark_sunglasses": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f576.png",
    "dart": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3af.png",
    "dash": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4a8.png",
    "date": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4c5.png",
    "de": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e9-1f1ea.png",
    "deciduous_tree": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f333.png",
    "deer": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f98c.png",
    "denmark": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e9-1f1f0.png",
    "department_store": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3ec.png",
    "derelict_house": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3da.png",
    "desert": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3dc.png",
    "desert_island": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3dd.png",
    "desktop_computer": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5a5.png",
    "detective": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f575.png",
    "diamond_shape_with_a_dot_inside": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4a0.png",
    "diamonds": "https://assets-cdn.github.com/images/icons/emoji/unicode/2666.png",
    "disappointed": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f61e.png",
    "disappointed_relieved": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f625.png",
    "dizzy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4ab.png",
    "dizzy_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f635.png",
    "djibouti": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e9-1f1ef.png",
    "do_not_litter": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6af.png",
    "dog": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f436.png",
    "dog2": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f415.png",
    "dollar": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4b5.png",
    "dolls": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f38e.png",
    "dolphin": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f42c.png",
    "dominica": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e9-1f1f2.png",
    "dominican_republic": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e9-1f1f4.png",
    "door": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6aa.png",
    "doughnut": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f369.png",
    "dove": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f54a.png",
    "dragon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f409.png",
    "dragon_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f432.png",
    "dress": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f457.png",
    "dromedary_camel": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f42a.png",
    "drooling_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f924.png",
    "droplet": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4a7.png",
    "drum": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f941.png",
    "duck": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f986.png",
    "dvd": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4c0.png",
    "e-mail": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4e7.png",
    "eagle": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f985.png",
    "ear": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f442.png",
    "ear_of_rice": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f33e.png",
    "earth_africa": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f30d.png",
    "earth_americas": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f30e.png",
    "earth_asia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f30f.png",
    "ecuador": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ea-1f1e8.png",
    "egg": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f95a.png",
    "eggplant": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f346.png",
    "egypt": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ea-1f1ec.png",
    "eight": "https://assets-cdn.github.com/images/icons/emoji/unicode/0038-20e3.png",
    "eight_pointed_black_star": "https://assets-cdn.github.com/images/icons/emoji/unicode/2734.png",
    "eight_spoked_asterisk": "https://assets-cdn.github.com/images/icons/emoji/unicode/2733.png",
    "el_salvador": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f8-1f1fb.png",
    "electric_plug": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f50c.png",
    "elephant": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f418.png",
    "email": "https://assets-cdn.github.com/images/icons/emoji/unicode/2709.png",
    "end": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f51a.png",
    "envelope": "https://assets-cdn.github.com/images/icons/emoji/unicode/2709.png",
    "envelope_with_arrow": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4e9.png",
    "equatorial_guinea": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ec-1f1f6.png",
    "eritrea": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ea-1f1f7.png",
    "es": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ea-1f1f8.png",
    "estonia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ea-1f1ea.png",
    "ethiopia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ea-1f1f9.png",
    "eu": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ea-1f1fa.png",
    "euro": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4b6.png",
    "european_castle": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3f0.png",
    "european_post_office": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3e4.png",
    "european_union": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ea-1f1fa.png",
    "evergreen_tree": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f332.png",
    "exclamation": "https://assets-cdn.github.com/images/icons/emoji/unicode/2757.png",
    "expressionless": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f611.png",
    "eye": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f441.png",
    "eye_speech_bubble": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f441-1f5e8.png",
    "eyeglasses": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f453.png",
    "eyes": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f440.png",
    "face_with_head_bandage": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f915.png",
    "face_with_thermometer": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f912.png",
    "facepunch": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f44a.png",
    "factory": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3ed.png",
    "falkland_islands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1eb-1f1f0.png",
    "fallen_leaf": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f342.png",
    "family": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f46a.png",
    "family_man_boy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f466.png",
    "family_man_boy_boy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f466-1f466.png",
    "family_man_girl": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f467.png",
    "family_man_girl_boy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f467-1f466.png",
    "family_man_girl_girl": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f467-1f467.png",
    "family_man_man_boy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f468-1f466.png",
    "family_man_man_boy_boy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f468-1f466-1f466.png",
    "family_man_man_girl": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f468-1f467.png",
    "family_man_man_girl_boy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f468-1f467-1f466.png",
    "family_man_man_girl_girl": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f468-1f467-1f467.png",
    "family_man_woman_boy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f46a.png",
    "family_man_woman_boy_boy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f469-1f466-1f466.png",
    "family_man_woman_girl": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f469-1f467.png",
    "family_man_woman_girl_boy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f469-1f467-1f466.png",
    "family_man_woman_girl_girl": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f469-1f467-1f467.png",  # noqa
    "family_woman_boy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f466.png",
    "family_woman_boy_boy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f466-1f466.png",
    "family_woman_girl": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f467.png",
    "family_woman_girl_boy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f467-1f466.png",
    "family_woman_girl_girl": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f467-1f467.png",
    "family_woman_woman_boy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f469-1f466.png",
    "family_woman_woman_boy_boy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f469-1f466-1f466.png",  # noqa
    "family_woman_woman_girl": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f469-1f467.png",
    "family_woman_woman_girl_boy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f469-1f467-1f466.png",  # noqa
    "family_woman_woman_girl_girl": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f469-1f467-1f467.png",  # noqa
    "faroe_islands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1eb-1f1f4.png",
    "fast_forward": "https://assets-cdn.github.com/images/icons/emoji/unicode/23e9.png",
    "fax": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4e0.png",
    "fearful": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f628.png",
    "feelsgood": "https://assets-cdn.github.com/images/icons/emoji/feelsgood.png",
    "feet": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f43e.png",
    "female_detective": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f575-2640.png",
    "ferris_wheel": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3a1.png",
    "ferry": "https://assets-cdn.github.com/images/icons/emoji/unicode/26f4.png",
    "field_hockey": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3d1.png",
    "fiji": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1eb-1f1ef.png",
    "file_cabinet": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5c4.png",
    "file_folder": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4c1.png",
    "film_projector": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4fd.png",
    "film_strip": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f39e.png",
    "finland": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1eb-1f1ee.png",
    "finnadie": "https://assets-cdn.github.com/images/icons/emoji/finnadie.png",
    "fire": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f525.png",
    "fire_engine": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f692.png",
    "fireworks": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f386.png",
    "first_quarter_moon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f313.png",
    "first_quarter_moon_with_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f31b.png",
    "fish": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f41f.png",
    "fish_cake": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f365.png",
    "fishing_pole_and_fish": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3a3.png",
    "fist": "https://assets-cdn.github.com/images/icons/emoji/unicode/270a.png",
    "fist_left": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f91b.png",
    "fist_oncoming": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f44a.png",
    "fist_raised": "https://assets-cdn.github.com/images/icons/emoji/unicode/270a.png",
    "fist_right": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f91c.png",
    "five": "https://assets-cdn.github.com/images/icons/emoji/unicode/0035-20e3.png",
    "flags": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f38f.png",
    "flashlight": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f526.png",
    "fleur_de_lis": "https://assets-cdn.github.com/images/icons/emoji/unicode/269c.png",
    "flight_arrival": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6ec.png",
    "flight_departure": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6eb.png",
    "flipper": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f42c.png",
    "floppy_disk": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4be.png",
    "flower_playing_cards": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3b4.png",
    "flushed": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f633.png",
    "fog": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f32b.png",
    "foggy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f301.png",
    "football": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3c8.png",
    "footprints": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f463.png",
    "fork_and_knife": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f374.png",
    "fountain": "https://assets-cdn.github.com/images/icons/emoji/unicode/26f2.png",
    "fountain_pen": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f58b.png",
    "four": "https://assets-cdn.github.com/images/icons/emoji/unicode/0034-20e3.png",
    "four_leaf_clover": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f340.png",
    "fox_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f98a.png",
    "fr": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1eb-1f1f7.png",
    "framed_picture": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5bc.png",
    "free": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f193.png",
    "french_guiana": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ec-1f1eb.png",
    "french_polynesia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f5-1f1eb.png",
    "french_southern_territories": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f9-1f1eb.png",
    "fried_egg": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f373.png",
    "fried_shrimp": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f364.png",
    "fries": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f35f.png",
    "frog": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f438.png",
    "frowning": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f626.png",
    "frowning_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/2639.png",
    "frowning_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f64d-2642.png",
    "frowning_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f64d.png",
    "fu": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f595.png",
    "fuelpump": "https://assets-cdn.github.com/images/icons/emoji/unicode/26fd.png",
    "full_moon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f315.png",
    "full_moon_with_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f31d.png",
    "funeral_urn": "https://assets-cdn.github.com/images/icons/emoji/unicode/26b1.png",
    "gabon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ec-1f1e6.png",
    "gambia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ec-1f1f2.png",
    "game_die": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3b2.png",
    "gb": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ec-1f1e7.png",
    "gear": "https://assets-cdn.github.com/images/icons/emoji/unicode/2699.png",
    "gem": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f48e.png",
    "gemini": "https://assets-cdn.github.com/images/icons/emoji/unicode/264a.png",
    "georgia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ec-1f1ea.png",
    "ghana": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ec-1f1ed.png",
    "ghost": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f47b.png",
    "gibraltar": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ec-1f1ee.png",
    "gift": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f381.png",
    "gift_heart": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f49d.png",
    "girl": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f467.png",
    "globe_with_meridians": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f310.png",
    "goal_net": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f945.png",
    "goat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f410.png",
    "goberserk": "https://assets-cdn.github.com/images/icons/emoji/goberserk.png",
    "godmode": "https://assets-cdn.github.com/images/icons/emoji/godmode.png",
    "golf": "https://assets-cdn.github.com/images/icons/emoji/unicode/26f3.png",
    "golfing_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3cc.png",
    "golfing_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3cc-2640.png",
    "gorilla": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f98d.png",
    "grapes": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f347.png",
    "greece": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ec-1f1f7.png",
    "green_apple": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f34f.png",
    "green_book": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4d7.png",
    "green_heart": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f49a.png",
    "green_salad": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f957.png",
    "greenland": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ec-1f1f1.png",
    "grenada": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ec-1f1e9.png",
    "grey_exclamation": "https://assets-cdn.github.com/images/icons/emoji/unicode/2755.png",
    "grey_question": "https://assets-cdn.github.com/images/icons/emoji/unicode/2754.png",
    "grimacing": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f62c.png",
    "grin": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f601.png",
    "grinning": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f600.png",
    "guadeloupe": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ec-1f1f5.png",
    "guam": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ec-1f1fa.png",
    "guardsman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f482.png",
    "guardswoman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f482-2640.png",
    "guatemala": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ec-1f1f9.png",
    "guernsey": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ec-1f1ec.png",
    "guinea": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ec-1f1f3.png",
    "guinea_bissau": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ec-1f1fc.png",
    "guitar": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3b8.png",
    "gun": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f52b.png",
    "guyana": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ec-1f1fe.png",
    "haircut": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f487.png",
    "haircut_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f487-2642.png",
    "haircut_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f487.png",
    "haiti": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ed-1f1f9.png",
    "hamburger": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f354.png",
    "hammer": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f528.png",
    "hammer_and_pick": "https://assets-cdn.github.com/images/icons/emoji/unicode/2692.png",
    "hammer_and_wrench": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6e0.png",
    "hamster": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f439.png",
    "hand": "https://assets-cdn.github.com/images/icons/emoji/unicode/270b.png",
    "handbag": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f45c.png",
    "handshake": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f91d.png",
    "hankey": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4a9.png",
    "hash": "https://assets-cdn.github.com/images/icons/emoji/unicode/0023-20e3.png",
    "hatched_chick": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f425.png",
    "hatching_chick": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f423.png",
    "headphones": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3a7.png",
    "hear_no_evil": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f649.png",
    "heart": "https://assets-cdn.github.com/images/icons/emoji/unicode/2764.png",
    "heart_decoration": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f49f.png",
    "heart_eyes": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f60d.png",
    "heart_eyes_cat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f63b.png",
    "heartbeat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f493.png",
    "heartpulse": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f497.png",
    "hearts": "https://assets-cdn.github.com/images/icons/emoji/unicode/2665.png",
    "heavy_check_mark": "https://assets-cdn.github.com/images/icons/emoji/unicode/2714.png",
    "heavy_division_sign": "https://assets-cdn.github.com/images/icons/emoji/unicode/2797.png",
    "heavy_dollar_sign": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4b2.png",
    "heavy_exclamation_mark": "https://assets-cdn.github.com/images/icons/emoji/unicode/2757.png",
    "heavy_heart_exclamation": "https://assets-cdn.github.com/images/icons/emoji/unicode/2763.png",
    "heavy_minus_sign": "https://assets-cdn.github.com/images/icons/emoji/unicode/2796.png",
    "heavy_multiplication_x": "https://assets-cdn.github.com/images/icons/emoji/unicode/2716.png",
    "heavy_plus_sign": "https://assets-cdn.github.com/images/icons/emoji/unicode/2795.png",
    "helicopter": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f681.png",
    "herb": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f33f.png",
    "hibiscus": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f33a.png",
    "high_brightness": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f506.png",
    "high_heel": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f460.png",
    "hocho": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f52a.png",
    "hole": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f573.png",
    "honduras": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ed-1f1f3.png",
    "honey_pot": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f36f.png",
    "honeybee": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f41d.png",
    "hong_kong": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ed-1f1f0.png",
    "horse": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f434.png",
    "horse_racing": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3c7.png",
    "hospital": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3e5.png",
    "hot_pepper": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f336.png",
    "hotdog": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f32d.png",
    "hotel": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3e8.png",
    "hotsprings": "https://assets-cdn.github.com/images/icons/emoji/unicode/2668.png",
    "hourglass": "https://assets-cdn.github.com/images/icons/emoji/unicode/231b.png",
    "hourglass_flowing_sand": "https://assets-cdn.github.com/images/icons/emoji/unicode/23f3.png",
    "house": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3e0.png",
    "house_with_garden": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3e1.png",
    "houses": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3d8.png",
    "hugs": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f917.png",
    "hungary": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ed-1f1fa.png",
    "hurtrealbad": "https://assets-cdn.github.com/images/icons/emoji/hurtrealbad.png",
    "hushed": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f62f.png",
    "ice_cream": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f368.png",
    "ice_hockey": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3d2.png",
    "ice_skate": "https://assets-cdn.github.com/images/icons/emoji/unicode/26f8.png",
    "icecream": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f366.png",
    "iceland": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ee-1f1f8.png",
    "id": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f194.png",
    "ideograph_advantage": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f250.png",
    "imp": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f47f.png",
    "inbox_tray": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4e5.png",
    "incoming_envelope": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4e8.png",
    "india": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ee-1f1f3.png",
    "indonesia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ee-1f1e9.png",
    "information_desk_person": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f481.png",
    "information_source": "https://assets-cdn.github.com/images/icons/emoji/unicode/2139.png",
    "innocent": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f607.png",
    "interrobang": "https://assets-cdn.github.com/images/icons/emoji/unicode/2049.png",
    "iphone": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4f1.png",
    "iran": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ee-1f1f7.png",
    "iraq": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ee-1f1f6.png",
    "ireland": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ee-1f1ea.png",
    "isle_of_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ee-1f1f2.png",
    "israel": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ee-1f1f1.png",
    "it": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ee-1f1f9.png",
    "izakaya_lantern": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3ee.png",
    "jack_o_lantern": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f383.png",
    "jamaica": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ef-1f1f2.png",
    "japan": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5fe.png",
    "japanese_castle": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3ef.png",
    "japanese_goblin": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f47a.png",
    "japanese_ogre": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f479.png",
    "jeans": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f456.png",
    "jersey": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ef-1f1ea.png",
    "jordan": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ef-1f1f4.png",
    "joy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f602.png",
    "joy_cat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f639.png",
    "joystick": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f579.png",
    "jp": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ef-1f1f5.png",
    "kaaba": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f54b.png",
    "kazakhstan": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f0-1f1ff.png",
    "kenya": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f0-1f1ea.png",
    "key": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f511.png",
    "keyboard": "https://assets-cdn.github.com/images/icons/emoji/unicode/2328.png",
    "keycap_ten": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f51f.png",
    "kick_scooter": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6f4.png",
    "kimono": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f458.png",
    "kiribati": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f0-1f1ee.png",
    "kiss": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f48b.png",
    "kissing": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f617.png",
    "kissing_cat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f63d.png",
    "kissing_closed_eyes": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f61a.png",
    "kissing_heart": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f618.png",
    "kissing_smiling_eyes": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f619.png",
    "kiwi_fruit": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f95d.png",
    "knife": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f52a.png",
    "koala": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f428.png",
    "koko": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f201.png",
    "kosovo": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1fd-1f1f0.png",
    "kr": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f0-1f1f7.png",
    "kuwait": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f0-1f1fc.png",
    "kyrgyzstan": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f0-1f1ec.png",
    "label": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3f7.png",
    "lantern": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3ee.png",
    "laos": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f1-1f1e6.png",
    "large_blue_circle": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f535.png",
    "large_blue_diamond": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f537.png",
    "large_orange_diamond": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f536.png",
    "last_quarter_moon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f317.png",
    "last_quarter_moon_with_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f31c.png",
    "latin_cross": "https://assets-cdn.github.com/images/icons/emoji/unicode/271d.png",
    "latvia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f1-1f1fb.png",
    "laughing": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f606.png",
    "leaves": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f343.png",
    "lebanon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f1-1f1e7.png",
    "ledger": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4d2.png",
    "left_luggage": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6c5.png",
    "left_right_arrow": "https://assets-cdn.github.com/images/icons/emoji/unicode/2194.png",
    "leftwards_arrow_with_hook": "https://assets-cdn.github.com/images/icons/emoji/unicode/21a9.png",
    "lemon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f34b.png",
    "leo": "https://assets-cdn.github.com/images/icons/emoji/unicode/264c.png",
    "leopard": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f406.png",
    "lesotho": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f1-1f1f8.png",
    "level_slider": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f39a.png",
    "liberia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f1-1f1f7.png",
    "libra": "https://assets-cdn.github.com/images/icons/emoji/unicode/264e.png",
    "libya": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f1-1f1fe.png",
    "liechtenstein": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f1-1f1ee.png",
    "light_rail": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f688.png",
    "link": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f517.png",
    "lion": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f981.png",
    "lips": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f444.png",
    "lipstick": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f484.png",
    "lithuania": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f1-1f1f9.png",
    "lizard": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f98e.png",
    "lock": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f512.png",
    "lock_with_ink_pen": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f50f.png",
    "lollipop": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f36d.png",
    "loop": "https://assets-cdn.github.com/images/icons/emoji/unicode/27bf.png",
    "loud_sound": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f50a.png",
    "loudspeaker": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4e2.png",
    "love_hotel": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3e9.png",
    "love_letter": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f48c.png",
    "low_brightness": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f505.png",
    "luxembourg": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f1-1f1fa.png",
    "lying_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f925.png",
    "m": "https://assets-cdn.github.com/images/icons/emoji/unicode/24c2.png",
    "macau": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1f4.png",
    "macedonia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1f0.png",
    "madagascar": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1ec.png",
    "mag": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f50d.png",
    "mag_right": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f50e.png",
    "mahjong": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f004.png",
    "mailbox": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4eb.png",
    "mailbox_closed": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4ea.png",
    "mailbox_with_mail": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4ec.png",
    "mailbox_with_no_mail": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4ed.png",
    "malawi": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1fc.png",
    "malaysia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1fe.png",
    "maldives": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1fb.png",
    "male_detective": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f575.png",
    "mali": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1f1.png",
    "malta": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1f9.png",
    "man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468.png",
    "man_artist": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f3a8.png",
    "man_astronaut": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f680.png",
    "man_cartwheeling": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f938-2642.png",
    "man_cook": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f373.png",
    "man_dancing": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f57a.png",
    "man_facepalming": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f926-2642.png",
    "man_factory_worker": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f3ed.png",
    "man_farmer": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f33e.png",
    "man_firefighter": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f692.png",
    "man_health_worker": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-2695.png",
    "man_in_tuxedo": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f935.png",
    "man_judge": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-2696.png",
    "man_juggling": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f939-2642.png",
    "man_mechanic": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f527.png",
    "man_office_worker": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f4bc.png",
    "man_pilot": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-2708.png",
    "man_playing_handball": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f93e-2642.png",
    "man_playing_water_polo": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f93d-2642.png",
    "man_scientist": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f52c.png",
    "man_shrugging": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f937-2642.png",
    "man_singer": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f3a4.png",
    "man_student": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f393.png",
    "man_teacher": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f3eb.png",
    "man_technologist": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f468-1f4bb.png",
    "man_with_gua_pi_mao": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f472.png",
    "man_with_turban": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f473.png",
    "mandarin": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f34a.png",
    "mans_shoe": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f45e.png",
    "mantelpiece_clock": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f570.png",
    "maple_leaf": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f341.png",
    "marshall_islands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1ed.png",
    "martial_arts_uniform": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f94b.png",
    "martinique": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1f6.png",
    "mask": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f637.png",
    "massage": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f486.png",
    "massage_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f486-2642.png",
    "massage_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f486.png",
    "mauritania": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1f7.png",
    "mauritius": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1fa.png",
    "mayotte": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1fe-1f1f9.png",
    "meat_on_bone": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f356.png",
    "medal_military": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f396.png",
    "medal_sports": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3c5.png",
    "mega": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4e3.png",
    "melon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f348.png",
    "memo": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4dd.png",
    "men_wrestling": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f93c-2642.png",
    "menorah": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f54e.png",
    "mens": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6b9.png",
    "metal": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f918.png",
    "metro": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f687.png",
    "mexico": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1fd.png",
    "micronesia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1eb-1f1f2.png",
    "microphone": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3a4.png",
    "microscope": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f52c.png",
    "middle_finger": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f595.png",
    "milk_glass": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f95b.png",
    "milky_way": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f30c.png",
    "minibus": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f690.png",
    "minidisc": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4bd.png",
    "mobile_phone_off": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4f4.png",
    "moldova": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1e9.png",
    "monaco": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1e8.png",
    "money_mouth_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f911.png",
    "money_with_wings": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4b8.png",
    "moneybag": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4b0.png",
    "mongolia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1f3.png",
    "monkey": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f412.png",
    "monkey_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f435.png",
    "monorail": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f69d.png",
    "montenegro": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1ea.png",
    "montserrat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1f8.png",
    "moon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f314.png",
    "morocco": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1e6.png",
    "mortar_board": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f393.png",
    "mosque": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f54c.png",
    "motor_boat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6e5.png",
    "motor_scooter": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6f5.png",
    "motorcycle": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3cd.png",
    "motorway": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6e3.png",
    "mount_fuji": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5fb.png",
    "mountain": "https://assets-cdn.github.com/images/icons/emoji/unicode/26f0.png",
    "mountain_bicyclist": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6b5.png",
    "mountain_biking_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6b5.png",
    "mountain_biking_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6b5-2640.png",
    "mountain_cableway": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6a0.png",
    "mountain_railway": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f69e.png",
    "mountain_snow": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3d4.png",
    "mouse": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f42d.png",
    "mouse2": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f401.png",
    "movie_camera": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3a5.png",
    "moyai": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5ff.png",
    "mozambique": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1ff.png",
    "mrs_claus": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f936.png",
    "muscle": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4aa.png",
    "mushroom": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f344.png",
    "musical_keyboard": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3b9.png",
    "musical_note": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3b5.png",
    "musical_score": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3bc.png",
    "mute": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f507.png",
    "myanmar": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1f2.png",
    "nail_care": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f485.png",
    "name_badge": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4db.png",
    "namibia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f3-1f1e6.png",
    "national_park": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3de.png",
    "nauru": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f3-1f1f7.png",
    "nauseated_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f922.png",
    "neckbeard": "https://assets-cdn.github.com/images/icons/emoji/neckbeard.png",
    "necktie": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f454.png",
    "negative_squared_cross_mark": "https://assets-cdn.github.com/images/icons/emoji/unicode/274e.png",
    "nepal": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f3-1f1f5.png",
    "nerd_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f913.png",
    "netherlands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f3-1f1f1.png",
    "neutral_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f610.png",
    "new": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f195.png",
    "new_caledonia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f3-1f1e8.png",
    "new_moon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f311.png",
    "new_moon_with_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f31a.png",
    "new_zealand": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f3-1f1ff.png",
    "newspaper": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4f0.png",
    "newspaper_roll": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5de.png",
    "next_track_button": "https://assets-cdn.github.com/images/icons/emoji/unicode/23ed.png",
    "ng": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f196.png",
    "ng_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f645-2642.png",
    "ng_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f645.png",
    "nicaragua": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f3-1f1ee.png",
    "niger": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f3-1f1ea.png",
    "nigeria": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f3-1f1ec.png",
    "night_with_stars": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f303.png",
    "nine": "https://assets-cdn.github.com/images/icons/emoji/unicode/0039-20e3.png",
    "niue": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f3-1f1fa.png",
    "no_bell": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f515.png",
    "no_bicycles": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6b3.png",
    "no_entry": "https://assets-cdn.github.com/images/icons/emoji/unicode/26d4.png",
    "no_entry_sign": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6ab.png",
    "no_good": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f645.png",
    "no_good_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f645-2642.png",
    "no_good_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f645.png",
    "no_mobile_phones": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4f5.png",
    "no_mouth": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f636.png",
    "no_pedestrians": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6b7.png",
    "no_smoking": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6ad.png",
    "non-potable_water": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6b1.png",
    "norfolk_island": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f3-1f1eb.png",
    "north_korea": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f0-1f1f5.png",
    "northern_mariana_islands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f2-1f1f5.png",
    "norway": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f3-1f1f4.png",
    "nose": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f443.png",
    "notebook": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4d3.png",
    "notebook_with_decorative_cover": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4d4.png",
    "notes": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3b6.png",
    "nut_and_bolt": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f529.png",
    "o": "https://assets-cdn.github.com/images/icons/emoji/unicode/2b55.png",
    "o2": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f17e.png",
    "ocean": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f30a.png",
    "octocat": "https://assets-cdn.github.com/images/icons/emoji/octocat.png",
    "octopus": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f419.png",
    "oden": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f362.png",
    "office": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3e2.png",
    "oil_drum": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6e2.png",
    "ok": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f197.png",
    "ok_hand": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f44c.png",
    "ok_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f646-2642.png",
    "ok_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f646.png",
    "old_key": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5dd.png",
    "older_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f474.png",
    "older_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f475.png",
    "om": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f549.png",
    "oman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f4-1f1f2.png",
    "on": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f51b.png",
    "oncoming_automobile": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f698.png",
    "oncoming_bus": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f68d.png",
    "oncoming_police_car": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f694.png",
    "oncoming_taxi": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f696.png",
    "one": "https://assets-cdn.github.com/images/icons/emoji/unicode/0031-20e3.png",
    "open_book": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4d6.png",
    "open_file_folder": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4c2.png",
    "open_hands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f450.png",
    "open_mouth": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f62e.png",
    "open_umbrella": "https://assets-cdn.github.com/images/icons/emoji/unicode/2602.png",
    "ophiuchus": "https://assets-cdn.github.com/images/icons/emoji/unicode/26ce.png",
    "orange": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f34a.png",
    "orange_book": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4d9.png",
    "orthodox_cross": "https://assets-cdn.github.com/images/icons/emoji/unicode/2626.png",
    "outbox_tray": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4e4.png",
    "owl": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f989.png",
    "ox": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f402.png",
    "package": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4e6.png",
    "page_facing_up": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4c4.png",
    "page_with_curl": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4c3.png",
    "pager": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4df.png",
    "paintbrush": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f58c.png",
    "pakistan": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f5-1f1f0.png",
    "palau": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f5-1f1fc.png",
    "palestinian_territories": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f5-1f1f8.png",
    "palm_tree": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f334.png",
    "panama": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f5-1f1e6.png",
    "pancakes": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f95e.png",
    "panda_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f43c.png",
    "paperclip": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4ce.png",
    "paperclips": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f587.png",
    "papua_new_guinea": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f5-1f1ec.png",
    "paraguay": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f5-1f1fe.png",
    "parasol_on_ground": "https://assets-cdn.github.com/images/icons/emoji/unicode/26f1.png",
    "parking": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f17f.png",
    "part_alternation_mark": "https://assets-cdn.github.com/images/icons/emoji/unicode/303d.png",
    "partly_sunny": "https://assets-cdn.github.com/images/icons/emoji/unicode/26c5.png",
    "passenger_ship": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6f3.png",
    "passport_control": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6c2.png",
    "pause_button": "https://assets-cdn.github.com/images/icons/emoji/unicode/23f8.png",
    "paw_prints": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f43e.png",
    "peace_symbol": "https://assets-cdn.github.com/images/icons/emoji/unicode/262e.png",
    "peach": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f351.png",
    "peanuts": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f95c.png",
    "pear": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f350.png",
    "pen": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f58a.png",
    "pencil": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4dd.png",
    "pencil2": "https://assets-cdn.github.com/images/icons/emoji/unicode/270f.png",
    "penguin": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f427.png",
    "pensive": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f614.png",
    "performing_arts": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3ad.png",
    "persevere": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f623.png",
    "person_fencing": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f93a.png",
    "person_frowning": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f64d.png",
    "person_with_blond_hair": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f471.png",
    "person_with_pouting_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f64e.png",
    "peru": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f5-1f1ea.png",
    "philippines": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f5-1f1ed.png",
    "phone": "https://assets-cdn.github.com/images/icons/emoji/unicode/260e.png",
    "pick": "https://assets-cdn.github.com/images/icons/emoji/unicode/26cf.png",
    "pig": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f437.png",
    "pig2": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f416.png",
    "pig_nose": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f43d.png",
    "pill": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f48a.png",
    "pineapple": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f34d.png",
    "ping_pong": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3d3.png",
    "pisces": "https://assets-cdn.github.com/images/icons/emoji/unicode/2653.png",
    "pitcairn_islands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f5-1f1f3.png",
    "pizza": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f355.png",
    "place_of_worship": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6d0.png",
    "plate_with_cutlery": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f37d.png",
    "play_or_pause_button": "https://assets-cdn.github.com/images/icons/emoji/unicode/23ef.png",
    "point_down": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f447.png",
    "point_left": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f448.png",
    "point_right": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f449.png",
    "point_up": "https://assets-cdn.github.com/images/icons/emoji/unicode/261d.png",
    "point_up_2": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f446.png",
    "poland": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f5-1f1f1.png",
    "police_car": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f693.png",
    "policeman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f46e.png",
    "policewoman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f46e-2640.png",
    "poodle": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f429.png",
    "poop": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4a9.png",
    "popcorn": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f37f.png",
    "portugal": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f5-1f1f9.png",
    "post_office": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3e3.png",
    "postal_horn": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4ef.png",
    "postbox": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4ee.png",
    "potable_water": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6b0.png",
    "potato": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f954.png",
    "pouch": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f45d.png",
    "poultry_leg": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f357.png",
    "pound": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4b7.png",
    "pout": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f621.png",
    "pouting_cat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f63e.png",
    "pouting_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f64e-2642.png",
    "pouting_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f64e.png",
    "pray": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f64f.png",
    "prayer_beads": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4ff.png",
    "pregnant_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f930.png",
    "previous_track_button": "https://assets-cdn.github.com/images/icons/emoji/unicode/23ee.png",
    "prince": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f934.png",
    "princess": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f478.png",
    "printer": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5a8.png",
    "puerto_rico": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f5-1f1f7.png",
    "punch": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f44a.png",
    "purple_heart": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f49c.png",
    "purse": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f45b.png",
    "pushpin": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4cc.png",
    "put_litter_in_its_place": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6ae.png",
    "qatar": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f6-1f1e6.png",
    "question": "https://assets-cdn.github.com/images/icons/emoji/unicode/2753.png",
    "rabbit": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f430.png",
    "rabbit2": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f407.png",
    "racehorse": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f40e.png",
    "racing_car": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3ce.png",
    "radio": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4fb.png",
    "radio_button": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f518.png",
    "radioactive": "https://assets-cdn.github.com/images/icons/emoji/unicode/2622.png",
    "rage": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f621.png",
    "rage1": "https://assets-cdn.github.com/images/icons/emoji/rage1.png",
    "rage2": "https://assets-cdn.github.com/images/icons/emoji/rage2.png",
    "rage3": "https://assets-cdn.github.com/images/icons/emoji/rage3.png",
    "rage4": "https://assets-cdn.github.com/images/icons/emoji/rage4.png",
    "railway_car": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f683.png",
    "railway_track": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6e4.png",
    "rainbow": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f308.png",
    "rainbow_flag": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3f3-1f308.png",
    "raised_back_of_hand": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f91a.png",
    "raised_hand": "https://assets-cdn.github.com/images/icons/emoji/unicode/270b.png",
    "raised_hand_with_fingers_splayed": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f590.png",
    "raised_hands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f64c.png",
    "raising_hand": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f64b.png",
    "raising_hand_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f64b-2642.png",
    "raising_hand_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f64b.png",
    "ram": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f40f.png",
    "ramen": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f35c.png",
    "rat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f400.png",
    "record_button": "https://assets-cdn.github.com/images/icons/emoji/unicode/23fa.png",
    "recycle": "https://assets-cdn.github.com/images/icons/emoji/unicode/267b.png",
    "red_car": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f697.png",
    "red_circle": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f534.png",
    "registered": "https://assets-cdn.github.com/images/icons/emoji/unicode/00ae.png",
    "relaxed": "https://assets-cdn.github.com/images/icons/emoji/unicode/263a.png",
    "relieved": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f60c.png",
    "reminder_ribbon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f397.png",
    "repeat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f501.png",
    "repeat_one": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f502.png",
    "rescue_worker_helmet": "https://assets-cdn.github.com/images/icons/emoji/unicode/26d1.png",
    "restroom": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6bb.png",
    "reunion": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f7-1f1ea.png",
    "revolving_hearts": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f49e.png",
    "rewind": "https://assets-cdn.github.com/images/icons/emoji/unicode/23ea.png",
    "rhinoceros": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f98f.png",
    "ribbon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f380.png",
    "rice": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f35a.png",
    "rice_ball": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f359.png",
    "rice_cracker": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f358.png",
    "rice_scene": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f391.png",
    "right_anger_bubble": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5ef.png",
    "ring": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f48d.png",
    "robot": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f916.png",
    "rocket": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f680.png",
    "rofl": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f923.png",
    "roll_eyes": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f644.png",
    "roller_coaster": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3a2.png",
    "romania": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f7-1f1f4.png",
    "rooster": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f413.png",
    "rose": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f339.png",
    "rosette": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3f5.png",
    "rotating_light": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6a8.png",
    "round_pushpin": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4cd.png",
    "rowboat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6a3.png",
    "rowing_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6a3.png",
    "rowing_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6a3-2640.png",
    "ru": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f7-1f1fa.png",
    "rugby_football": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3c9.png",
    "runner": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3c3.png",
    "running": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3c3.png",
    "running_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3c3.png",
    "running_shirt_with_sash": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3bd.png",
    "running_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3c3-2640.png",
    "rwanda": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f7-1f1fc.png",
    "sa": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f202.png",
    "sagittarius": "https://assets-cdn.github.com/images/icons/emoji/unicode/2650.png",
    "sailboat": "https://assets-cdn.github.com/images/icons/emoji/unicode/26f5.png",
    "sake": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f376.png",
    "samoa": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1fc-1f1f8.png",
    "san_marino": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f8-1f1f2.png",
    "sandal": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f461.png",
    "santa": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f385.png",
    "sao_tome_principe": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f8-1f1f9.png",
    "satellite": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4e1.png",
    "satisfied": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f606.png",
    "saudi_arabia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f8-1f1e6.png",
    "saxophone": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3b7.png",
    "school": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3eb.png",
    "school_satchel": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f392.png",
    "scissors": "https://assets-cdn.github.com/images/icons/emoji/unicode/2702.png",
    "scorpion": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f982.png",
    "scorpius": "https://assets-cdn.github.com/images/icons/emoji/unicode/264f.png",
    "scream": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f631.png",
    "scream_cat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f640.png",
    "scroll": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4dc.png",
    "seat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4ba.png",
    "secret": "https://assets-cdn.github.com/images/icons/emoji/unicode/3299.png",
    "see_no_evil": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f648.png",
    "seedling": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f331.png",
    "selfie": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f933.png",
    "senegal": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f8-1f1f3.png",
    "serbia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f7-1f1f8.png",
    "seven": "https://assets-cdn.github.com/images/icons/emoji/unicode/0037-20e3.png",
    "seychelles": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f8-1f1e8.png",
    "shallow_pan_of_food": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f958.png",
    "shamrock": "https://assets-cdn.github.com/images/icons/emoji/unicode/2618.png",
    "shark": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f988.png",
    "shaved_ice": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f367.png",
    "sheep": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f411.png",
    "shell": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f41a.png",
    "shield": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6e1.png",
    "shinto_shrine": "https://assets-cdn.github.com/images/icons/emoji/unicode/26e9.png",
    "ship": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6a2.png",
    "shipit": "https://assets-cdn.github.com/images/icons/emoji/shipit.png",
    "shirt": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f455.png",
    "shit": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4a9.png",
    "shoe": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f45e.png",
    "shopping": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6cd.png",
    "shopping_cart": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6d2.png",
    "shower": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6bf.png",
    "shrimp": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f990.png",
    "sierra_leone": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f8-1f1f1.png",
    "signal_strength": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4f6.png",
    "singapore": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f8-1f1ec.png",
    "sint_maarten": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f8-1f1fd.png",
    "six": "https://assets-cdn.github.com/images/icons/emoji/unicode/0036-20e3.png",
    "six_pointed_star": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f52f.png",
    "ski": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3bf.png",
    "skier": "https://assets-cdn.github.com/images/icons/emoji/unicode/26f7.png",
    "skull": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f480.png",
    "skull_and_crossbones": "https://assets-cdn.github.com/images/icons/emoji/unicode/2620.png",
    "sleeping": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f634.png",
    "sleeping_bed": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6cc.png",
    "sleepy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f62a.png",
    "slightly_frowning_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f641.png",
    "slightly_smiling_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f642.png",
    "slot_machine": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3b0.png",
    "slovakia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f8-1f1f0.png",
    "slovenia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f8-1f1ee.png",
    "small_airplane": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6e9.png",
    "small_blue_diamond": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f539.png",
    "small_orange_diamond": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f538.png",
    "small_red_triangle": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f53a.png",
    "small_red_triangle_down": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f53b.png",
    "smile": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f604.png",
    "smile_cat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f638.png",
    "smiley": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f603.png",
    "smiley_cat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f63a.png",
    "smiling_imp": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f608.png",
    "smirk": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f60f.png",
    "smirk_cat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f63c.png",
    "smoking": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6ac.png",
    "snail": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f40c.png",
    "snake": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f40d.png",
    "sneezing_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f927.png",
    "snowboarder": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3c2.png",
    "snowflake": "https://assets-cdn.github.com/images/icons/emoji/unicode/2744.png",
    "snowman": "https://assets-cdn.github.com/images/icons/emoji/unicode/26c4.png",
    "snowman_with_snow": "https://assets-cdn.github.com/images/icons/emoji/unicode/2603.png",
    "sob": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f62d.png",
    "soccer": "https://assets-cdn.github.com/images/icons/emoji/unicode/26bd.png",
    "solomon_islands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f8-1f1e7.png",
    "somalia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f8-1f1f4.png",
    "soon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f51c.png",
    "sos": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f198.png",
    "sound": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f509.png",
    "south_africa": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ff-1f1e6.png",
    "south_georgia_south_sandwich_islands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ec-1f1f8.png",
    "south_sudan": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f8-1f1f8.png",
    "space_invader": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f47e.png",
    "spades": "https://assets-cdn.github.com/images/icons/emoji/unicode/2660.png",
    "spaghetti": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f35d.png",
    "sparkle": "https://assets-cdn.github.com/images/icons/emoji/unicode/2747.png",
    "sparkler": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f387.png",
    "sparkles": "https://assets-cdn.github.com/images/icons/emoji/unicode/2728.png",
    "sparkling_heart": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f496.png",
    "speak_no_evil": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f64a.png",
    "speaker": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f508.png",
    "speaking_head": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5e3.png",
    "speech_balloon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4ac.png",
    "speedboat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6a4.png",
    "spider": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f577.png",
    "spider_web": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f578.png",
    "spiral_calendar": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5d3.png",
    "spiral_notepad": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5d2.png",
    "spoon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f944.png",
    "squid": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f991.png",
    "squirrel": "https://assets-cdn.github.com/images/icons/emoji/shipit.png",
    "sri_lanka": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f1-1f1f0.png",
    "st_barthelemy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e7-1f1f1.png",
    "st_helena": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f8-1f1ed.png",
    "st_kitts_nevis": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f0-1f1f3.png",
    "st_lucia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f1-1f1e8.png",
    "st_pierre_miquelon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f5-1f1f2.png",
    "st_vincent_grenadines": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1fb-1f1e8.png",
    "stadium": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3df.png",
    "star": "https://assets-cdn.github.com/images/icons/emoji/unicode/2b50.png",
    "star2": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f31f.png",
    "star_and_crescent": "https://assets-cdn.github.com/images/icons/emoji/unicode/262a.png",
    "star_of_david": "https://assets-cdn.github.com/images/icons/emoji/unicode/2721.png",
    "stars": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f320.png",
    "station": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f689.png",
    "statue_of_liberty": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5fd.png",
    "steam_locomotive": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f682.png",
    "stew": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f372.png",
    "stop_button": "https://assets-cdn.github.com/images/icons/emoji/unicode/23f9.png",
    "stop_sign": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6d1.png",
    "stopwatch": "https://assets-cdn.github.com/images/icons/emoji/unicode/23f1.png",
    "straight_ruler": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4cf.png",
    "strawberry": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f353.png",
    "stuck_out_tongue": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f61b.png",
    "stuck_out_tongue_closed_eyes": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f61d.png",
    "stuck_out_tongue_winking_eye": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f61c.png",
    "studio_microphone": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f399.png",
    "stuffed_flatbread": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f959.png",
    "sudan": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f8-1f1e9.png",
    "sun_behind_large_cloud": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f325.png",
    "sun_behind_rain_cloud": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f326.png",
    "sun_behind_small_cloud": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f324.png",
    "sun_with_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f31e.png",
    "sunflower": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f33b.png",
    "sunglasses": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f60e.png",
    "sunny": "https://assets-cdn.github.com/images/icons/emoji/unicode/2600.png",
    "sunrise": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f305.png",
    "sunrise_over_mountains": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f304.png",
    "surfer": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3c4.png",
    "surfing_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3c4.png",
    "surfing_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3c4-2640.png",
    "suriname": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f8-1f1f7.png",
    "sushi": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f363.png",
    "suspect": "https://assets-cdn.github.com/images/icons/emoji/suspect.png",
    "suspension_railway": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f69f.png",
    "swaziland": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f8-1f1ff.png",
    "sweat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f613.png",
    "sweat_drops": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4a6.png",
    "sweat_smile": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f605.png",
    "sweden": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f8-1f1ea.png",
    "sweet_potato": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f360.png",
    "swimmer": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3ca.png",
    "swimming_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3ca.png",
    "swimming_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3ca-2640.png",
    "switzerland": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e8-1f1ed.png",
    "symbols": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f523.png",
    "synagogue": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f54d.png",
    "syria": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f8-1f1fe.png",
    "syringe": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f489.png",
    "taco": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f32e.png",
    "tada": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f389.png",
    "taiwan": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f9-1f1fc.png",
    "tajikistan": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f9-1f1ef.png",
    "tanabata_tree": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f38b.png",
    "tangerine": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f34a.png",
    "tanzania": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f9-1f1ff.png",
    "taurus": "https://assets-cdn.github.com/images/icons/emoji/unicode/2649.png",
    "taxi": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f695.png",
    "tea": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f375.png",
    "telephone": "https://assets-cdn.github.com/images/icons/emoji/unicode/260e.png",
    "telephone_receiver": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4de.png",
    "telescope": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f52d.png",
    "tennis": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3be.png",
    "tent": "https://assets-cdn.github.com/images/icons/emoji/unicode/26fa.png",
    "thailand": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f9-1f1ed.png",
    "thermometer": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f321.png",
    "thinking": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f914.png",
    "thought_balloon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4ad.png",
    "three": "https://assets-cdn.github.com/images/icons/emoji/unicode/0033-20e3.png",
    "thumbsdown": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f44e.png",
    "thumbsup": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f44d.png",
    "ticket": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3ab.png",
    "tickets": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f39f.png",
    "tiger": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f42f.png",
    "tiger2": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f405.png",
    "timer_clock": "https://assets-cdn.github.com/images/icons/emoji/unicode/23f2.png",
    "timor_leste": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f9-1f1f1.png",
    "tipping_hand_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f481-2642.png",
    "tipping_hand_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f481.png",
    "tired_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f62b.png",
    "tm": "https://assets-cdn.github.com/images/icons/emoji/unicode/2122.png",
    "togo": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f9-1f1ec.png",
    "toilet": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6bd.png",
    "tokelau": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f9-1f1f0.png",
    "tokyo_tower": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5fc.png",
    "tomato": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f345.png",
    "tonga": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f9-1f1f4.png",
    "tongue": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f445.png",
    "top": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f51d.png",
    "tophat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3a9.png",
    "tornado": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f32a.png",
    "tr": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f9-1f1f7.png",
    "trackball": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5b2.png",
    "tractor": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f69c.png",
    "traffic_light": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6a5.png",
    "train": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f68b.png",
    "train2": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f686.png",
    "tram": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f68a.png",
    "triangular_flag_on_post": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6a9.png",
    "triangular_ruler": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4d0.png",
    "trident": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f531.png",
    "trinidad_tobago": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f9-1f1f9.png",
    "triumph": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f624.png",
    "trolleybus": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f68e.png",
    "trollface": "https://assets-cdn.github.com/images/icons/emoji/trollface.png",
    "trophy": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3c6.png",
    "tropical_drink": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f379.png",
    "tropical_fish": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f420.png",
    "truck": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f69a.png",
    "trumpet": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3ba.png",
    "tshirt": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f455.png",
    "tulip": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f337.png",
    "tumbler_glass": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f943.png",
    "tunisia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f9-1f1f3.png",
    "turkey": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f983.png",
    "turkmenistan": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f9-1f1f2.png",
    "turks_caicos_islands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f9-1f1e8.png",
    "turtle": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f422.png",
    "tuvalu": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1f9-1f1fb.png",
    "tv": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4fa.png",
    "twisted_rightwards_arrows": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f500.png",
    "two": "https://assets-cdn.github.com/images/icons/emoji/unicode/0032-20e3.png",
    "two_hearts": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f495.png",
    "two_men_holding_hands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f46c.png",
    "two_women_holding_hands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f46d.png",
    "u5272": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f239.png",
    "u5408": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f234.png",
    "u55b6": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f23a.png",
    "u6307": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f22f.png",
    "u6708": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f237.png",
    "u6709": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f236.png",
    "u6e80": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f235.png",
    "u7121": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f21a.png",
    "u7533": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f238.png",
    "u7981": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f232.png",
    "u7a7a": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f233.png",
    "uganda": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1fa-1f1ec.png",
    "uk": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ec-1f1e7.png",
    "ukraine": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1fa-1f1e6.png",
    "umbrella": "https://assets-cdn.github.com/images/icons/emoji/unicode/2614.png",
    "unamused": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f612.png",
    "underage": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f51e.png",
    "unicorn": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f984.png",
    "united_arab_emirates": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1e6-1f1ea.png",
    "unlock": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f513.png",
    "up": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f199.png",
    "upside_down_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f643.png",
    "uruguay": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1fa-1f1fe.png",
    "us": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1fa-1f1f8.png",
    "us_virgin_islands": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1fb-1f1ee.png",
    "uzbekistan": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1fa-1f1ff.png",
    "v": "https://assets-cdn.github.com/images/icons/emoji/unicode/270c.png",
    "vanuatu": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1fb-1f1fa.png",
    "vatican_city": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1fb-1f1e6.png",
    "venezuela": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1fb-1f1ea.png",
    "vertical_traffic_light": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6a6.png",
    "vhs": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4fc.png",
    "vibration_mode": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4f3.png",
    "video_camera": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4f9.png",
    "video_game": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3ae.png",
    "vietnam": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1fb-1f1f3.png",
    "violin": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3bb.png",
    "virgo": "https://assets-cdn.github.com/images/icons/emoji/unicode/264d.png",
    "volcano": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f30b.png",
    "volleyball": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3d0.png",
    "vs": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f19a.png",
    "vulcan_salute": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f596.png",
    "walking": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6b6.png",
    "walking_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6b6.png",
    "walking_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6b6-2640.png",
    "wallis_futuna": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1fc-1f1eb.png",
    "waning_crescent_moon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f318.png",
    "waning_gibbous_moon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f316.png",
    "warning": "https://assets-cdn.github.com/images/icons/emoji/unicode/26a0.png",
    "wastebasket": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5d1.png",
    "watch": "https://assets-cdn.github.com/images/icons/emoji/unicode/231a.png",
    "water_buffalo": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f403.png",
    "watermelon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f349.png",
    "wave": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f44b.png",
    "wavy_dash": "https://assets-cdn.github.com/images/icons/emoji/unicode/3030.png",
    "waxing_crescent_moon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f312.png",
    "waxing_gibbous_moon": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f314.png",
    "wc": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6be.png",
    "weary": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f629.png",
    "wedding": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f492.png",
    "weight_lifting_man": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3cb.png",
    "weight_lifting_woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3cb-2640.png",
    "western_sahara": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ea-1f1ed.png",
    "whale": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f433.png",
    "whale2": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f40b.png",
    "wheel_of_dharma": "https://assets-cdn.github.com/images/icons/emoji/unicode/2638.png",
    "wheelchair": "https://assets-cdn.github.com/images/icons/emoji/unicode/267f.png",
    "white_check_mark": "https://assets-cdn.github.com/images/icons/emoji/unicode/2705.png",
    "white_circle": "https://assets-cdn.github.com/images/icons/emoji/unicode/26aa.png",
    "white_flag": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f3f3.png",
    "white_flower": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4ae.png",
    "white_large_square": "https://assets-cdn.github.com/images/icons/emoji/unicode/2b1c.png",
    "white_medium_small_square": "https://assets-cdn.github.com/images/icons/emoji/unicode/25fd.png",
    "white_medium_square": "https://assets-cdn.github.com/images/icons/emoji/unicode/25fb.png",
    "white_small_square": "https://assets-cdn.github.com/images/icons/emoji/unicode/25ab.png",
    "white_square_button": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f533.png",
    "wilted_flower": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f940.png",
    "wind_chime": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f390.png",
    "wind_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f32c.png",
    "wine_glass": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f377.png",
    "wink": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f609.png",
    "wolf": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f43a.png",
    "woman": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469.png",
    "woman_artist": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f3a8.png",
    "woman_astronaut": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f680.png",
    "woman_cartwheeling": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f938-2640.png",
    "woman_cook": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f373.png",
    "woman_facepalming": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f926-2640.png",
    "woman_factory_worker": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f3ed.png",
    "woman_farmer": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f33e.png",
    "woman_firefighter": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f692.png",
    "woman_health_worker": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-2695.png",
    "woman_judge": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-2696.png",
    "woman_juggling": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f939-2640.png",
    "woman_mechanic": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f527.png",
    "woman_office_worker": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f4bc.png",
    "woman_pilot": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-2708.png",
    "woman_playing_handball": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f93e-2640.png",
    "woman_playing_water_polo": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f93d-2640.png",
    "woman_scientist": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f52c.png",
    "woman_shrugging": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f937-2640.png",
    "woman_singer": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f3a4.png",
    "woman_student": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f393.png",
    "woman_teacher": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f3eb.png",
    "woman_technologist": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f469-1f4bb.png",
    "woman_with_turban": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f473-2640.png",
    "womans_clothes": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f45a.png",
    "womans_hat": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f452.png",
    "women_wrestling": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f93c-2640.png",
    "womens": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f6ba.png",
    "world_map": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f5fa.png",
    "worried": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f61f.png",
    "wrench": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f527.png",
    "writing_hand": "https://assets-cdn.github.com/images/icons/emoji/unicode/270d.png",
    "x": "https://assets-cdn.github.com/images/icons/emoji/unicode/274c.png",
    "yellow_heart": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f49b.png",
    "yemen": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1fe-1f1ea.png",
    "yen": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4b4.png",
    "yin_yang": "https://assets-cdn.github.com/images/icons/emoji/unicode/262f.png",
    "yum": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f60b.png",
    "zambia": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ff-1f1f2.png",
    "zap": "https://assets-cdn.github.com/images/icons/emoji/unicode/26a1.png",
    "zero": "https://assets-cdn.github.com/images/icons/emoji/unicode/0030-20e3.png",
    "zimbabwe": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f1ff-1f1fc.png",
    "zipper_mouth_face": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f910.png",
    "zzz": "https://assets-cdn.github.com/images/icons/emoji/unicode/1f4a4.png"
}
# --end--


def get_github_emoji():  # pragma: no cover
    """Get Github's usable emoji."""

    try:
        resp = requests.get(
            'https://api.github.com/emojis',
            timeout=30
        )
    except Exception:
        return None

    return json.loads(resp.text)


def update_emoji():  # pragma: no cover
    """Update the emoji pattern in memory."""

    global RE_EMOJI
    global URL_EMOJI

    emoji_list = get_github_emoji()
    emoji_map = {}

    if emoji_list is not None:
        for emoji in emoji_list:
            url = emoji_list[emoji]
            m = RE_ASSET.match(url)
            if m:
                emoji_map[emoji] = m.group('image')

    if emoji_map:
        RE_EMOJI = ':(%s):' % '|'.join([re.escape(key) for key in sorted(emoji_map.keys())])
        URL_EMOJI = copy.copy(emoji_map)


class SimpleEmojiPattern(Pattern):
    """Return element of type `tag` with a text attribute of group(3) of a Pattern."""

    def __init__(self, pattern, css_class='emoji'):
        """Initialize."""

        self.css_class = css_class
        Pattern.__init__(self, pattern)

    def handleMatch(self, m):
        """Hanlde emoji pattern matches."""

        attributes = {
            "src": URL_EMOJI[m.group(2)],
            "alt": ":%s:" % m.group(2),
            "title": ":%s:" % m.group(2),
            "height": "20px",
            "width": "20px",
            "align": "absmiddle"
        }

        if self.css_class:
            attributes['class'] = self.css_class

        el = util.etree.Element("img", attributes)
        return el


class GithubEmojiExtension(Extension):
    """Add emoji extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'css_class': [
                "emoji",
                "CSS class name to add to emoji images.  Use an empty string if you want no class"
                "- Default: 'emoji'"
            ],
            'offline': [
                True,
                "Uses the pre-built emoji list. Will not connect to the internet.  If 'False' "
                "githubemoji will pull down the latest list url format via github's API. "
                "Really only needed if the list is out of date and you must get the latest. "
                "- Default: True"
            ]
        }

        warnings.warn(
            "The pymdownx.githubemoji Extension is pending deprecation. Use the pymdownx.emoji Extension instead.",
            PendingDeprecationWarning
        )

        super(GithubEmojiExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Add support for <del>test</del> tags as ~~test~~."""
        if not self.getConfigs()['offline'] and USE_REQUESTS:  # pragma: no cover
            update_emoji()
        css_class = self.getConfigs()["css_class"]
        md.inlinePatterns.add("github-emoji", SimpleEmojiPattern(RE_EMOJI, css_class), "<not_strong")


def makeExtension(*args, **kwargs):
    """Return extension."""

    return GithubEmojiExtension(*args, **kwargs)


if __name__ == "__main__":  # pragma: no cover
    # Update the emoji pattern in this file.

    import codecs
    import os

    file_name = os.path.abspath(__file__)

    def get_latest_emoji():
        """Get the latest emoji list."""

        # Update the file's regex pattern
        emoji_list = get_github_emoji()
        emoji_map = {}

        if emoji_list is not None:
            for emoji in emoji_list:
                url = emoji_list[emoji]
                m = RE_ASSET.match(url)
                if m:
                    emoji_map[emoji] = m.group('image')

        return emoji_map

    def update_emoji_source(file_name, emoji_map):
        """Update *this* source file with the latest emoji."""

        if emoji_map:
            replacement = None
            start = None
            end = None

            with codecs.open(file_name, 'r', encoding='utf-8') as f:
                m = re.match(r'(.*?# --start--\r?\n).*?(# --end--.*)', f.read(), re.DOTALL)
                if m:
                    start = m.group(1)
                    end = m.group(2)
                    replacement = 'RE_EMOJI = r\'\'\'(?x)\n:('
                    first = True
                    line = ''
                    for name in sorted(emoji_map.keys()):
                        escaped = re.escape(name)
                        if first:
                            first = False
                            sep = ''
                        else:
                            sep = '|'
                        if (len(line) + len(escaped) + len(sep)) > 110:
                            replacement += '\n    ' + line
                            line = ''
                        line += sep + escaped
                    replacement += '\n    ' + line + '\n):\'\'\'\n'
                    replacement += '\nURL_EMOJI = {'
                    first = True
                    for name in sorted(emoji_map.keys()):
                        if first:
                            first = False
                        else:
                            replacement += ','
                        replacement += '\n    "%s": "%s"' % (name, emoji_map[name])
                    replacement += '\n}\n'

            assert replacement is not None, "No emoji :("

            with codecs.open(file_name, 'w', encoding='utf-8') as f:
                f.write(start + replacement + end)

    try:
        emoji_map = get_latest_emoji()
        update_emoji_source(file_name, emoji_map)
        print('PASS - Emoji updated :)')
    except Exception as e:
        print(e)
        print('FAIL - No emoji :(')

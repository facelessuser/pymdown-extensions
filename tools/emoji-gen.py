"""
Generates emoji regex file.

Names are manually coppied from http://www.emoji-cheat-sheet.com/ and formatted in the array.
When called, they are sorted and output as python regex that can be coppied and pasted.

One day, the names should be acquired automatically and output directly into a python file.
"""
emoji = [
    [
        'People',
        'bowtie,smile,laughing,blush,smiley,relaxed,smirk,heart_eyes,kissing_heart,kissing_closed_eyes,flushed,relieved'
        ',satisfied,grin,wink,stuck_out_tongue_winking_eye,stuck_out_tongue_closed_eyes,grinning,kissing,kissing_smilin'
        'g_eyes,stuck_out_tongue,sleeping,worried,frowning,anguished,open_mouth,grimacing,confused,hushed,expressionles'
        's,unamused,sweat_smile,sweat,disappointed_relieved,weary,pensive,disappointed,confounded,fearful,cold_sweat,pe'
        'rsevere,cry,sob,joy,astonished,scream,neckbeard,tired_face,angry,rage,triumph,sleepy,yum,mask,sunglasses,dizzy'
        '_face,imp,smiling_imp,neutral_face,no_mouth,innocent,alien,yellow_heart,blue_heart,purple_heart,heart,green_he'
        'art,broken_heart,heartbeat,heartpulse,two_hearts,revolving_hearts,cupid,sparkling_heart,sparkles,star,star2,di'
        'zzy,boom,collision,anger,exclamation,question,grey_exclamation,grey_question,zzz,dash,sweat_drops,notes,musica'
        'l_note,fire,hankey,poop,shit,+1,thumbsup,-1,thumbsdown,ok_hand,punch,facepunch,fist,v,wave,hand,raised_hand,op'
        'en_hands,point_up,point_down,point_left,point_right,raised_hands,pray,point_up_2,clap,muscle,metal,fu,walking,'
        'runner,running,couple,family,two_men_holding_hands,two_women_holding_hands,dancer,dancers,ok_woman,no_good,inf'
        'ormation_desk_person,raising_hand,bride_with_veil,person_with_pouting_face,person_frowning,bow,couplekiss,coup'
        'le_with_heart,massage,haircut,nail_care,boy,girl,woman,man,baby,older_woman,older_man,person_with_blond_hair,m'
        'an_with_gua_pi_mao,man_with_turban,construction_worker,cop,angel,princess,smiley_cat,smile_cat,heart_eyes_cat,'
        'kissing_cat,smirk_cat,scream_cat,crying_cat_face,joy_cat,pouting_cat,japanese_ogre,japanese_goblin,see_no_evil'
        ',hear_no_evil,speak_no_evil,guardsman,skull,feet,lips,kiss,droplet,ear,eyes,nose,tongue,love_letter,bust_in_si'
        'lhouette,busts_in_silhouette,speech_balloon,thought_balloon,feelsgood,finnadie,goberserk,godmode,hurtrealbad,r'
        'age1,rage2,rage3,rage4,suspect,trollface'.split(',')
    ],
    [
        'Nature',
        'sunny,umbrella,cloud,snowflake,snowman,zap,cyclone,foggy,ocean,cat,dog,mouse,hamster,rabbit,wolf,frog,tiger,ko'
        'ala,bear,bee,pig,pig_nose,cow,boar,monkey_face,monkey,horse,racehorse,camel,sheep,elephant,panda_face,snake,bi'
        'rd,baby_chick,hatched_chick,hatching_chick,chicken,penguin,turtle,bug,honeybee,ant,beetle,snail,octopus,tropic'
        'al_fish,fish,whale,whale2,dolphin,cow2,ram,rat,water_buffalo,tiger2,rabbit2,dragon,goat,rooster,dog2,pig2,mous'
        'e2,ox,dragon_face,blowfish,crocodile,dromedary_camel,leopard,cat2,poodle,paw_prints,bouquet,cherry_blossom,tul'
        'ip,four_leaf_clover,rose,sunflower,hibiscus,maple_leaf,leaves,fallen_leaf,herb,mushroom,cactus,palm_tree,everg'
        'reen_tree,deciduous_tree,chestnut,seedling,blossom,ear_of_rice,shell,globe_with_meridians,sun_with_face,full_m'
        'oon_with_face,new_moon_with_face,new_moon,waxing_crescent_moon,crescent_moon,first_quarter_moon,waxing_gibbous'
        '_moon,full_moon,waning_gibbous_moon,last_quarter_moon,waning_crescent_moon,last_quarter_moon_with_face,first_q'
        'uarter_moon_with_face,moon,earth_africa,earth_americas,earth_asia,volcano,milky_way,partly_sunny,octocat,squir'
        'rel,night_with_stars'.split(',')
    ],
    [
        'Objects',
        'bamboo,gift_heart,dolls,school_satchel,mortar_board,flags,fireworks,sparkler,wind_chime,rice_scene,jack_o_lant'
        'ern,ghost,santa,christmas_tree,gift,bell,no_bell,tanabata_tree,tada,confetti_ball,balloon,crystal_ball,cd,dvd,'
        'floppy_disk,camera,video_camera,movie_camera,computer,tv,iphone,phone,telephone,telephone_receiver,pager,fax,m'
        'inidisc,vhs,sound,loud_sound,speaker,mute,loudspeaker,mega,hourglass,hourglass_flowing_sand,alarm_clock,watch,'
        'radio,satellite,loop,mag,mag_right,unlock,lock,lock_with_ink_pen,closed_lock_with_key,key,bulb,flashlight,high'
        '_brightness,low_brightness,electric_plug,battery,calling,e-mail,mailbox,postbox,bath,bathtub,shower,toilet,wre'
        'nch,nut_and_bolt,hammer,seat,moneybag,yen,dollar,pound,euro,credit_card,money_with_wings,email,inbox_tray,outb'
        'ox_tray,envelope,envelope_with_arrow,incoming_envelope,postal_horn,mailbox_closed,mailbox_with_mail,flipper,fo'
        'otprints,mailbox_with_no_mail,door,smoking,bomb,gun,hocho,pill,syringe,page_facing_up,page_with_curl,bookmark_'
        'tabs,bar_chart,chart_with_upwards_trend,chart_with_downwards_trend,scroll,clipboard,calendar,date,card_index,f'
        'ile_folder,open_file_folder,scissors,pushpin,paperclip,black_nib,pencil2,straight_ruler,triangular_ruler,close'
        'd_book,green_book,blue_book,orange_book,notebook,notebook_with_decorative_cover,ledger,books,bookmark,name_bad'
        'ge,microscope,telescope,newspaper,football,basketball,soccer,baseball,tennis,8ball,rugby_football,bowling,golf'
        ',mountain_bicyclist,bicyclist,horse_racing,snowboarder,swimmer,surfer,ski,spades,hearts,clubs,diamonds,gem,rin'
        'g,trophy,musical_score,musical_keyboard,violin,space_invader,video_game,black_joker,flower_playing_cards,game_'
        'die,dart,mahjong,clapper,memo,pencil,book,art,microphone,headphones,trumpet,saxophone,guitar,athletic_shoe,sho'
        'e,sandal,high_heel,lipstick,boot,shirt,tshirt,necktie,womans_clothes,dress,running_shirt_with_sash,jeans,kimon'
        'o,bikini,ribbon,tophat,crown,womans_hat,mans_shoe,closed_umbrella,briefcase,handbag,pouch,purse,eyeglasses,fis'
        'hing_pole_and_fish,coffee,tea,sake,baby_bottle,beer,beers,cocktail,tropical_drink,wine_glass,fork_and_knife,pi'
        'zza,hamburger,fries,poultry_leg,meat_on_bone,spaghetti,curry,fried_shrimp,bento,sushi,fish_cake,rice_ball,rice'
        '_cracker,rice,ramen,stew,oden,dango,egg,bread,doughnut,custard,icecream,ice_cream,shaved_ice,birthday,cake,coo'
        'kie,chocolate_bar,candy,lollipop,honey_pot,apple,green_apple,tangerine,lemon,cherries,grapes,watermelon,strawb'
        'erry,peach,melon,banana,pear,pineapple,sweet_potato,eggplant,tomato,corn,sparkle,package,open_book,lantern'
        ''.split(',')
    ],
    [
        'Places',
        'house,house_with_garden,school,office,post_office,hospital,bank,convenience_store,love_hotel,hotel,wedding,chu'
        'rch,department_store,european_post_office,city_sunrise,city_sunset,japanese_castle,european_castle,tent,factor'
        'y,tokyo_tower,japan,mount_fuji,sunrise_over_mountains,sunrise,stars,statue_of_liberty,bridge_at_night,carousel'
        '_horse,rainbow,ferris_wheel,fountain,roller_coaster,ship,speedboat,boat,sailboat,rowboat,anchor,rocket,airplan'
        'e,helicopter,steam_locomotive,tram,mountain_railway,bike,aerial_tramway,suspension_railway,mountain_cableway,t'
        'ractor,blue_car,oncoming_automobile,car,red_car,taxi,oncoming_taxi,articulated_lorry,bus,oncoming_bus,rotating'
        '_light,police_car,oncoming_police_car,fire_engine,ambulance,minibus,truck,train,station,train2,bullettrain_fro'
        'nt,bullettrain_side,light_rail,monorail,railway_car,trolleybus,ticket,fuelpump,vertical_traffic_light,traffic_'
        'light,warning,construction,beginner,atm,slot_machine,busstop,barber,hotsprings,checkered_flag,crossed_flags,iz'
        'akaya_lantern,moyai,circus_tent,performing_arts,round_pushpin,triangular_flag_on_post,jp,kr,cn,us,fr,es,it,ru,'
        'gb,uk,de'.split(',')
    ],
    [
        'Symbols',
        'one,two,three,four,five,six,seven,eight,nine,keycap_ten,1234,zero,hash,symbols,back,arrow_backward,arrow_down,'
        'arrow_forward,arrow_left,capital_abcd,abcd,abc,arrow_lower_left,arrow_lower_right,arrow_right,arrow_up,arrow_u'
        'pper_left,arrow_upper_right,arrow_double_down,arrow_double_up,arrow_down_small,arrow_heading_down,arrow_headin'
        'g_up,leftwards_arrow_with_hook,arrow_right_hook,left_right_arrow,arrow_up_down,arrow_up_small,arrows_clockwise'
        ',arrows_counterclockwise,rewind,fast_forward,information_source,ok,twisted_rightwards_arrows,repeat,repeat_one'
        ',new,top,up,cool,free,ng,cinema,koko,signal_strength,u5272,u5408,u55b6,u6307,u6708,u6709,u6e80,u7121,u7533,u7a'
        '7a,u7981,sa,restroom,mens,womens,baby_symbol,no_smoking,parking,wheelchair,metro,baggage_claim,accept,wc,potab'
        'le_water,put_litter_in_its_place,secret,congratulations,m,passport_control,left_luggage,customs,ideograph_adva'
        'ntage,cl,sos,id,no_entry_sign,underage,no_mobile_phones,do_not_litter,non-potable_water,no_bicycles,no_pedestr'
        'ians,children_crossing,no_entry,eight_spoked_asterisk,eight_pointed_black_star,heart_decoration,vs,vibration_m'
        'ode,mobile_phone_off,chart,currency_exchange,aries,taurus,gemini,cancer,leo,virgo,libra,scorpius,sagittarius,c'
        'apricorn,aquarius,pisces,ophiuchus,six_pointed_star,negative_squared_cross_mark,a,b,ab,o2,diamond_shape_with_a'
        '_dot_inside,recycle,end,on,soon,clock1,clock130,clock10,clock1030,clock11,clock1130,clock12,clock1230,clock2,c'
        'lock230,clock3,clock330,clock4,clock430,clock5,clock530,clock6,clock630,clock7,clock730,clock8,clock830,clock9'
        ',clock930,heavy_dollar_sign,copyright,registered,tm,x,heavy_exclamation_mark,bangbang,interrobang,o,heavy_mult'
        'iplication_x,heavy_plus_sign,heavy_minus_sign,heavy_division_sign,white_flower,100,heavy_check_mark,ballot_box'
        '_with_check,radio_button,link,curly_loop,wavy_dash,part_alternation_mark,trident,black_large_square,black_smal'
        'l_square,black_medium_square,black_medium_small_square,white_large_square,white_small_square,white_medium_squa'
        're,white_medium_small_square,white_check_mark,black_square_button,white_square_button,black_circle,white_circl'
        'e,red_circle,large_blue_circle,large_blue_diamond,large_orange_diamond,small_blue_diamond,small_orange_diamond'
        ',small_red_triangle,small_red_triangle_down,shipit'.split(',')
    ]
]


with open("emoji-test.md", "w") as f:
    for emoji_type in emoji:
        emoji_type[1].sort()
        f.write("### %s\n\n" % emoji_type[0].replace("_", " "))
        for e in emoji_type[1]:
            f.write(":%s:" % e)
        f.write("\n\n")

with open("emoji-regex.txt", "w") as f:
    for emoji_type in emoji:
        # emoji_type[1].sort()
        f.write("%s\n" % emoji_type[0].replace("_", " "))
        f.write(":(%s):" % '|'.join(emoji_type[1]).replace("+", "\\+"))
        f.write("\n\n")

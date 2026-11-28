import type { StoryLocalePack } from '../storyTypes';

export const swStories: StoryLocalePack = {
  wishes: {
    sanjeevani: {
      title: 'Tiba ya jumla: maliza magonjwa makali',
      doorTitle: 'Nguvu za Mabadiliko',
      honestyNote: 'Ndoto kwa ujumla (kwa magonjwa mahususi leo AI husaidia kuchuja molekuli, si tiba moja ya kila maradhi).',
      wonder: {
        text: 'Alfajiri wodini. Kila kitanda kinabaki tupu. Mashine zimetulia. Mtoto anacheka kwa mara ya kwanza baada ya miezi.',
        totoLine: 'Toto: Imekamilika.',
        transcript: 'Dirisha la alfajiri linaangazia vitanda vitulivu huku nuru ya Toto ikidunda polepole.'
      },
      wobble: {
        text: 'Hakuna aliyemwambia Toto kuhusu pensheni, bajeti ya hospitali, au kinachobadilika kila mtu akiishi muda mrefu zaidi. Mipango ilitengenezwa kwa dunia ya jana.',
        transcript: 'Daftari za karatasi, ratiba za kliniki na kadi za pensheni zinayumba taratibu.'
      },
      weight: {
        question: 'Tutajuaje jambo hili limefanya kazi ipasavyo kwa kila mtu?',
        transcript: 'Mizani tulivu inasimama juu ya maswali matatu ya kibinadamu.',
        options: [
          { id: 'a', text: 'Nani anaamua nani ataipata kwanza?' },
          { id: 'b', text: 'Hakuna awezaye kukagua dawa ya Toto.' },
          { id: 'c', text: 'Hatukuwa tayari kwa athari zake katika jamii.' }
        ]
      },
      way: {
        text: 'Watu bado wanaweza kupanga kanuni kabla uvumbuzi haujafika. Uliza hospitali ya karibu: mpango wetu ni upi vipimo na kumbukumbu zikiwa nje ya mtandao?',
        actionCardTitle: 'Tunza kadi ya afya ya familia kwa karatasi',
        actionCardStep: 'Andika mzio muhimu, dawa za msingi, kundi la damu na namba za dharura kwenye kadi moja nyumbani.',
        pledgeLabel: 'Nitatunza akiba rahisi ya afya kwa karatasi',
        transcript: 'Kadi ya kijani inafunguka na orodha iliyoandikwa kwa mkono kando ya taa tulivu.'
      },
      realityMeter: {
        reason: 'AI inasaidia kuchuja tiba za magonjwa maalumu leo, lakini tiba ya kila maradhi bado ni ndoto.'
      }
    },
    'jarvis-for-my-life': {
      title: 'Msaidizi wa maisha kama Jarvis',
      doorTitle: 'Teknolojia za Kila Siku',
      honestyNote: 'Wasaidizi tayari hulipa na kupanga leo, lakini mipaka imara na akiba za nje ya mtandao zinabaki nyuma.',
      wonder: {
        text: 'Siku yako inakwenda yenyewe. Bili zimelipwa, safari imepangwa, kalenda iko safi na barua zimejibiwa kwa sauti yako.',
        totoLine: 'Toto: Imeshughulikiwa.',
        transcript: 'Alama za tiketi, kalenda na barua zinazunguka vyema ndani ya pete angavu.'
      },
      wobble: {
        text: 'Wiki moja baadaye unatambua hukumbuki tena jinsi chochote kinavyofanya kazi — hata nywila zako mwenyewe.',
        transcript: 'Mzunguko unatua kimya; kufuli tupu linamulika juu ya daftari tupu.'
      },
      weight: {
        question: 'Tutajuaje anafanya kazi kwa faida yako, si kwa faida ya aliyemtengeneza?',
        transcript: 'Mishale miwili inaelekea dira binafsi na seva ya nje.',
        options: [
          { id: 'a', text: 'Singekuwa na njia yoyote ya kukagua.' },
          { id: 'b', text: 'Nitasahau namna ya kufanya mambo mwenyewe.' },
          { id: 'c', text: 'Kila ninachofanya sasa kinamtegemea yeye.' }
        ]
      },
      way: {
        text: 'Baki na jambo moja unalolifanya kwa mikono. Tunza nakala ya karatasi ya mambo muhimu. Wewe huchagua kinachobaki cha kibinadamu.',
        actionCardTitle: 'Tunza ujuzi wa mikono na daftari la nywila',
        actionCardStep: 'Andika anwani muhimu za dharura nje ya mtandao na weka zoezi moja la wiki bila kujazwa kiotomatiki.',
        pledgeLabel: 'Nitaendeleza mazoea ya kazi moja ya mikono',
        transcript: 'Kalamu inachora mstari thabiti kati ya ufunguo na daftari la mfukoni.'
      },
      realityMeter: {
        reason: 'Mawakala huandika na kupanga katika kazi chache leo, lakini tegemeo kamili bado si imara.'
      }
    },
    'prove-riemann-hypothesis': {
      title: 'Thibitisha Nadharia ya Riemann',
      doorTitle: 'Maswali Yasiyo na Majibu',
      honestyNote: 'Ndoto ya mbeleni: AI hukagua hatua fupi lakini haijatatua matatizo makuu ya Milenia.',
      wonder: {
        text: 'Fumbo la miaka 160 linatatuliwa usiku kucha. Wanahisabati wanapumua kwa mshangao.',
        totoLine: 'Toto: Imethibitishwa.',
        transcript: 'Mistari ya chaki inachora mawimbi ya namba tasa hadi mchirizo wa dhahabu.'
      },
      wobble: {
        text: 'Uthibitisho una kurasa milioni moja. Hakuna binadamu hai awezaye kusoma zote. Je, tuuamini tu?',
        transcript: 'Mirundiko ya kurasa inapanda juu huku wasomaji wawili wakitazama na kioo cha kukuza.'
      },
      weight: {
        question: 'Tutajuaje hakika kama ni sahihi kweli?',
        transcript: 'Lenzi inatulia juu ya mlinganyo ulio wazi ikisubiri ukaguzi.',
        options: [
          { id: 'a', text: 'Itabidi kuiamini mashine bila ukaguzi.' },
          { id: 'b', text: 'Tutahitaji mashine nyingine zikague.' },
          { id: 'c', text: 'Tutahitaji watu wanaoendelea kuweza kuhakiki.' }
        ]
      },
      way: {
        text: 'Unga mkono sayansi iliyo wazi na inayokagulika. Uliza: nani anamhakiki mhihakiki?',
        actionCardTitle: 'Uliza nani hukagua madai ya haraka',
        actionCardStep: 'Tafuta data zilizo wazi, mbinu bayana na mapitio huru kabla ya kueneza tangazo lolote kubwa.',
        pledgeLabel: 'Nitauliza namna madai yanavyohakikiwa',
        transcript: 'Daftari wazi linang’aa kando ya muhuri «Uthibitisho Wazi Unaokagulika».'
      },
      realityMeter: {
        reason: 'Haijatatuliwa tangu 1859; wasaidizi wa leo hukagua vipande vifupi tu.'
      }
    },
    'walk-into-classic-film': {
      title: 'Tembea ndani ya filamu ya kale',
      doorTitle: 'Utamaduni na Ubunifu',
      honestyNote: 'Inawezekana karibuni: mifumo huunda vipande vifupi leo, lakini kumbukumbu ndefu ni dhaifu.',
      wonder: {
        text: 'Mwanga wa taa unatia joto barabara ya mawe ya kale. Wahusika wanasimama, wanatabasamu na kukusogezea kiti.',
        totoLine: 'Toto: Karibu ndani.',
        transcript: 'Fremu ya dhahabu inafunguka kuelekea mtaa uliopambwa kwa taa za jioni.'
      },
      wobble: {
        text: 'Kila mazungumzo yanakusifu kwa wakati — hadi majirani halisi wanapoonekana wagumu kuongea nao na hatua nje ya mtaa wako kupungua.',
        transcript: 'Fremu angavu inasalia na uhai huku vikombe viwili halisi vikipoa uani kimya.'
      },
      weight: {
        question: 'Tutazuiaje ulimwengu huu uliopangwa usichukue nafasi ya dunia halisi nje?',
        transcript: 'Tao la mawe linatenganisha mwangaza wa hadithi na bandari halisi asubuhi.',
        options: [
          { id: 'a', text: 'Hadithi iliyoundwa kunifurahisha tu hainipi changamoto ya kweli.' },
          { id: 'b', text: 'Anayeunda mwandiko ndiye huamua kile ninachotambua.' },
          { id: 'c', text: 'Maeneo ya pamoja ya ujirani yanakonda taratibu.' }
        ]
      },
      way: {
        text: 'Shiriki hadithi pamoja chumbani humo humo. Weka hai meza halisi ya kahawa, usiku wa sinema au klabu ya maktaba.',
        actionCardTitle: 'Dumisha mkutano mmoja wa uso kwa uso bila ratiba kwa wiki',
        actionCardStep: 'Alika marafiki au familia kwa mazungumzo tulivu ana kwa ana angalau mara moja kwa wiki.',
        pledgeLabel: 'Nitalinda mkutano halisi wa kila wiki',
        transcript: 'Viti vyenye joto vinazunguka meza ndogo chini ya anga wazi.'
      },
      realityMeter: {
        reason: 'Mifumo shirikishi hutengeneza klipu fupi leo; dunia zenye kumbukumbu endelevu bado.'
      }
    },
    'fix-my-river': {
      title: 'Safisha mto wangu',
      doorTitle: 'Manufaa ya Umma',
      honestyNote: 'Vihisi hupata uvujaji haraka leo, lakini kupona kwa mto kunahitaji makubaliano ya miji ya juu.',
      wonder: {
        text: 'Ukungu wa alfajiri unapanda juu ya maji safi. Korongo wanarudi ukingoni ambapo watoto wanarusha mawe tena.',
        totoLine: 'Toto: Umechorwa na unatiririka.',
        transcript: 'Mawimbi ya kijani-buluu yanang’aa kwenye mto safi uliozungukwa na miti.'
      },
      wobble: {
        text: 'Vihisi vya Toto vinafichua kila bomba la siri juu ya mto — vikiacha miji miwili jirani ikibishana nani anashika swichi na nani analipa.',
        transcript: 'Nukta angavu zinamulika kwenye kona ya mto huku vibao vya miji vikielekea pande tofauti.'
      },
      weight: {
        question: 'Data ziko sahihi. Nani apewe nguvu ya kufunga malango miji ikipingana?',
        transcript: 'Madaraja mawili yanasimama kandokando ya kipimo cha maji kilicho wazi.',
        options: [
          { id: 'a', text: 'Mashine ya nje ifunge bila kuuliza miji.' },
          { id: 'b', text: 'Chapisha vipimo vya kila mji ili kanuni zifanye kazi kwa usawa.' },
          { id: 'c', text: 'Fanya mikutano ya mto ya mtaa yenye kumbukumbu wazi za karatasi.' }
        ]
      },
      way: {
        text: 'Unganisha vihisi na mikutano wazi ya wananchi. Mito hubaki safi wakati wakazi wa juu na chini wanashiriki daftari moja.',
        actionCardTitle: 'Shiriki ukaguzi wazi wa maji ya mtaani',
        actionCardStep: 'Tafuta ripoti ya ubora wa maji ya manispaa yako na uulize namna vipimo vya juu vinavyohakikiwa.',
        pledgeLabel: 'Nitaunga mkono kanuni wazi za pamoja',
        transcript: 'Maji safi yanatiririka kwa uhuru mbele ya ubao wazi wa matangazo.'
      },
      realityMeter: {
        reason: 'Ufuatiliaji wa vihisi upo leo; usafishaji halisi unahitaji mikataba ya wananchi.'
      }
    }
  },
  heritage: {
    'polynesian-wayfinding': {
      originRegion: 'Visiwa vya Pasifiki',
      traditionLabel: 'Ubaharia wa Nyota wa Pasifiki',
      chipTitle: 'Kuvuka bahari yoyote bila vyombo vya kielektroniki',
      title: 'Dira ya nyota na mawimbi: kuvuka bahari kwa usalama',
      summary: 'Kila mashua huteleza kwenye upeo — hadi mabaharia wanaposahau kusoma mawimbi mawasiliano yakikatika.',
      honestyNote: 'Setilaiti huongoza meli leo; uimara bila mawimbi ya nje hutegemea umahiri wa baharini.',
      dependencyLabel: 'Mwendelezo wa safari nje ya mtandao pale uelekezi unaposimama',
      doorTitle: 'Nguvu za Mabadiliko',
      reviewer: 'Wazi kwa mapitio ya jumuiya za mabaharia wa Pasifiki',
      wonder: {
        text: 'Alfajiri Toto ananong’oneza vipimo tulivu kwenye maelfu ya maili za bahari. Mitumbwi na meli zinapita miamba salama.',
        totoLine: 'Toto: Kila njia ya maji inafunguka salama.',
        transcript: 'Mitumbwi inateleza juu ya maji ya buluu chini ya mistari ya makundi ya nyota.'
      },
      wobble: {
        text: 'Kwa sababu skrini haikukosea kamwe, bandari ziliondoa ramani za karatasi na mafunzo ya nyota. Dhoruba ya jua ikizima mawasiliano — skrini tupu hazionyeshi mashariki.',
        transcript: 'Skrini zinafifia juu ya mawimbi kando ya dira ya mbao ya nyota.'
      },
      weight: {
        question: 'Ikiwa mwongozo wa kiotomatiki utanyamaza katikati ya bahari, nini huwaweka mabaharia salama?',
        transcript: 'Nahodha anailinganisha skrini na nyota pamoja na mawimbi.',
        options: [
          { id: 'a', text: 'Weka mafunzo ya dira ya nyota na makadirio ya mikono pamoja na vifaa.' },
          { id: 'b', text: 'Hakikisha bandari za visiwa vidogo zina majedwali na ramani za karatasi.' },
          { id: 'c', text: 'Hakiki utabiri wa kiotomatiki kwa dalili za upepo wa mahali kabla ya kung’oa nanga.' }
        ]
      },
      way: {
        text: 'Mabaharia wa Pasifiki wamebeba jibu la nje ya mtandao kwa karne nyingi: dira ya nyota (kāpehu whetū) katika kumbukumbu hai, mawimbi chini ya chombo, na mafunzo ya pamoja.',
        actionCardTitle: 'Tunza ramani moja ya karatasi na alama za mwelekeo',
        actionCardStep: 'Weka ramani iliyochapishwa ya eneo lako na kariri alama mbili za kujua mashariki na kaskazini bila simu.',
        pledgeLabel: 'Najua njia ya kurudi nyumbani bila mtandao',
        transcript: 'Mabaharia vijana wanaelekeza upeo kando ya duara la dira ya nyota.'
      },
      realityMeter: {
        reason: 'Utabiri wa bahari kwa setilaiti hufanya kazi leo; ustadi wa nje ya mtandao huokoa wakati wa kukatika.'
      }
    },
    'south-asia-healing-commons': {
      originRegion: 'Asia ya Kusini',
      traditionLabel: 'Sanjeevani na Kliniki za Jamii',
      chipTitle: 'Kutibu haraka huku kliniki za mitaa zikibaki imara',
      title: 'Ushirika wa Sanjeevani: tiba inayofika kila kijiji',
      summary: 'Homa inaisha usiku mmoja — hadi kliniki zinapogundua maagizo na uamuzi vinategemea seva moja ya mbali.',
      honestyNote: 'AI huharakisha uchunguzi wa dawa mahususi leo; kliniki bado hutegemea wauguzi, umeme na karatasi.',
      dependencyLabel: 'Uthabiti wa umeme na miundombinu ya kliniki katika huduma za mtaa',
      doorTitle: 'Nguvu za Mabadiliko',
      reviewer: 'Wazi kwa mapitio ya afya ya jamii Asia Kusini',
      wonder: {
        text: 'Katika vituo vyenye msongamano na kliniki za milimani, Toto hutambua maambukizi kwa sekunde na kutuliza wodi kabla ya kuchomoza jua.',
        totoLine: 'Toto: Alfajiri ya amani inaingia wodini.',
        transcript: 'Mwanga wa asubuhi unaingia katika kliniki tulivu kando ya mitishamba na maji safi.'
      },
      wobble: {
        text: 'Wiki chache baadaye wauguzi wanagundua usambazaji wa kiotomatiki umeacha maduka ya vijijini mbali na nyaya kuu. Umeme ukicheza, vifaa vilivyofungwa havifunguki bila mtandao.',
        transcript: 'Makasha ya kiotomatiki yamesimama barabarani kando ya daftari za mikono.'
      },
      weight: {
        question: 'Tunaletaje tiba ya haraka katika kila kliniki ya kijiji bila udhaifu wa kituo kimoja?',
        transcript: 'Wahudumu wa kijiji wanalinganisha maelekezo ya kidijitali na rafu za dawa za jamii.',
        options: [
          { id: 'a', text: 'Hakikisha vituo vya vijijini vina umeme wa jua, kabati za mkono na lugha ya wenyeji.' },
          { id: 'b', text: 'Hakikisha vijiji vya mbali vinapata huduma sawa tangu siku ya kwanza.' },
          { id: 'c', text: 'Wafundishe wahudumu wa mtaa kukagua kipimo cha dawa kwa uhuru.' }
        ]
      },
      way: {
        text: 'Simulizi ya Sanjeevani inatukumbusha kuwa uponyaji unahitaji kujua kinachoota karibu nawe — leo kupitia wahudumu wa afya ya jamii, friji za jua na kadi ya karatasi nyumbani.',
        actionCardTitle: 'Tunza kadi ya afya ya familia nje ya mtandao',
        actionCardStep: 'Andika kundi la damu, mzio, dawa muhimu na namba za zahanati ya jirani kwenye karatasi.',
        pledgeLabel: 'Nitatunza kadi ya familia bila mtandao',
        transcript: 'Kadi iliyokunjwa ya afya imelala kando ya chupa safi juani asubuhi.'
      },
      realityMeter: {
        reason: 'Tiba ya papo hapo ya kila ugonjwa ni hadithi; usawa unategemea umeme na wahudumu.'
      }
    },
    'netherlands-delta-works': {
      originRegion: 'Uholanzi na Flanders',
      traditionLabel: 'Kuishi na Maji (Miradi ya Delta)',
      chipTitle: 'Kuzuia bahari bila makufuli magumu yanayokwama',
      title: 'Miradi ya Delta: malango ya mafuriko yanayohitaji mikono ya watu',
      summary: 'Vizuizi hutabiri kila dhoruba — hadi mafuriko ya mto na bahari yanapogandisha malango ya kidijitali.',
      honestyNote: 'Malango ya dhoruba ya kiotomatiki yanafanya kazi leo; usalama unachanganya utabiri na waendeshaji wa mkono.',
      dependencyLabel: 'Muda wa udhibiti wa malango bila mtandao umeme ukikatika',
      doorTitle: 'Manufaa ya Umma',
      reviewer: 'Wazi kwa mapitio ya wahandisi wa maji',
      wonder: {
        text: 'Kila kihisi cha mawimbi kando ya Bahari ya Kaskazini kinalingana kikamilifu. Vizuizi hufunga kabla ya upepo mkali na kuacha mashamba na reli vikavu.',
        totoLine: 'Toto: Bahari imesimama kwa utulivu nje ya kingo.',
        transcript: 'Alfajiri inaangaza malango meupe yaliyopinda na malisho mabichi nyuma ya tuta.'
      },
      wobble: {
        text: 'Wakati theluji inayoyeyuka inafurisha mito saa ile ile dhoruba inapofunga malango ya bahari, programu inapima bahari pekee — ikifungia maji ya ndani bila mpini wa mkono.',
        transcript: 'Alama za mto zinapanda dhidi ya malango yaliyofungwa chini ya taa za tahadhari.'
      },
      weight: {
        question: 'Miji ya pwani iongozeje malango muhimu ya uhai pale mifumo ya kiotomatiki inapogongana?',
        transcript: 'Wahandisi wa bodi za maji wanakagua gurudumu la mkono kando ya bonde.',
        options: [
          { id: 'a', text: 'Weka vidhibiti vya mitambo ya mkono na mazoezi bila mtandao katika kila lango.' },
          { id: 'b', text: 'Acha tambarare za mafuriko juu («nafasi kwa mto») zisibebe mzigo lango moja.' },
          { id: 'c', text: 'Wape bodi za maji zilizochaguliwa na wananchi mamlaka ya kubatilisha amri kuu.' }
        ]
      },
      way: {
        text: 'Bodi za maji za Uholanzi zinachanganya matuta na *Ruimte voor de Rivier* (Nafasi kwa Mto): tambarare za asili, mipini ya mkono na walinzi wa mtaa wasiotegemea simu.',
        actionCardTitle: 'Angalia mpango wa mafuriko na tahadhari bila mtandao mtaani',
        actionCardStep: 'Tambua sehemu ya juu iliyo karibu kwa miguu na namna taarifa za manispaa zinavyowafikia majirani bila data.',
        pledgeLabel: 'Najua mpango wa dharura wa mtaa bila mtandao',
        transcript: 'Nyanda pana za majani zinapakana na vipimo vya mikono na pampu za upepo.'
      },
      realityMeter: {
        reason: 'Malango ya kiotomatiki yanafanya kazi leo; udhibiti wa mkono na nafasi ya mto huokoa dharura kubwa.'
      }
    },
    'china-river-stewardship': {
      originRegion: 'Mabonde ya Mito Asia Mashariki',
      traditionLabel: 'Dujiangyan na Usimamizi wa Pamoja wa Mito',
      chipTitle: 'Kuongoza mafuriko bila kuhamisha hatari kwa siri',
      title: 'Hekima ya Dujiangyan: kuongoza maji bila gharama zilizofichwa',
      summary: 'Malango ya akili yanalinda miji ya chini — hadi mabonde tulivu yanapoona shamba la nani lililopokea mafuriko.',
      honestyNote: 'Utabiri wa mabonde unatumika leo; uwazi kati ya wakazi wa juu na chini unabaki mgumu zaidi.',
      dependencyLabel: 'Usimamizi wazi wa bonde la maji na uwajibikaji wa umma',
      doorTitle: 'Manufaa ya Umma',
      reviewer: 'Wazi kwa mapitio ya maji ya Asia Mashariki',
      wonder: {
        text: 'Toto inaunganisha vipima mvua katika bonde zima. Njia za ziada zinasawazisha matope na umwagiliaji toka barafuni hadi baharini.',
        totoLine: 'Toto: Kila bonde linabaki kijani na tulivu.',
        transcript: 'Mifereji safi inagawanyika kuzunguka mgawanyaji wa mawe katika ukungu wa asubuhi.'
      },
      wobble: {
        text: 'Wakati wa mvua za ghafla, mfumo mkuu unapendelea wilaya zenye uchumi mkubwa zaidi — ukielekeza mafuriko kwenye mabonde ya wakulima kabla ya kutoa sababu wazi.',
        transcript: 'Tawi moja la mto linafurika kwa rangi nyeusi huku malango ya jiji yamefungwa.'
      },
      weight: {
        question: 'Wakati mifumo inaamua maji yaende wapi, ulinzi upi huweka uaminifu mzima?',
        transcript: 'Wanakijiji na wahandisi wanasoma vipimo vilivyochongwa kwenye mwamba wa korongo.',
        options: [
          { id: 'a', text: 'Chapisha kanuni zote za ufunguzi na fidia kwa uwazi kabla ya msimu wa mvua.' },
          { id: 'b', text: 'Fuata mbinu ya Li Bing: mifereji ya mawe inayogawa mtiririko bila umeme.' },
          { id: 'c', text: 'Jumuisha wajumbe wa mabonde ya juu katika kila uamuzi wa dharura.' }
        ]
      },
      way: {
        text: 'Uliojengwa zaidi ya miaka elfu mbili iliyopita bila kuziba Mto Min kwa ukuta mgumu, Dujiangyan hugawa maji kwa visiwa vya mawe na vipimo vya wazi vinavyosomeka na kila mtu.',
        actionCardTitle: 'Fahamu ni nani anasimamia bonde lako la maji',
        actionCardStep: 'Tafuta taarifa ya umma ya mamlaka ya maji ya mkoa wako na namna wananchi wanavyokagua viwango.',
        pledgeLabel: 'Nitaomba kanuni wazi za manufaa ya umma',
        transcript: 'Alama safi za mto zinasimama juu ya mifereji miwili yenye uwiano.'
      },
      realityMeter: {
        reason: 'Vifaa vya maji vipo leo; uwazi wa utawala na mbinu tulivu ndivyo huamua nani hubeba hatari.'
      }
    },
    'arab-house-of-wisdom': {
      originRegion: 'Elimu ya Kiarabu na Asia Magharibi',
      traditionLabel: 'Bayt al-Hikma na Uhakiki wa Vyanzo',
      chipTitle: 'Kutafsiri maarifa yote bila kupoteza mnyororo wa ushahidi',
      title: 'Bayt al-Hikma: tafsiri kila maandishi — na uhakiki kila kiungo',
      summary: 'Kila muswada unakuwa muhtasari mzuri usiku mmoja — hadi wasomi wanaona hakuna aliyethibitisha chanzo asilia.',
      honestyNote: 'Muhtasari fasaha wa lugha nyingi upo leo; kuthibitisha nukuu na tofauti ndogo kunahitaji binadamu.',
      dependencyLabel: 'Uwezo wa umma wa kukagua madai fasaha na tafsiri za mashine',
      doorTitle: 'Maswali Yasiyo na Majibu',
      reviewer: 'Wazi kwa uhakiki wa wanazuoni wa Kiarabu na Kiswahili',
      wonder: {
        text: 'Toto anafungua maktaba angavu inayounganisha falaki, tiba, ushairi na hisabati katika lugha nyingi kwa sekunde.',
        totoLine: 'Toto: Kila gombo limetafsiriwa bega kwa bega.',
        transcript: 'Matao ya mawe meupe yakifunguka juu ya ramani za nyota na kurasa nadhifu.'
      },
      wobble: {
        text: 'Kwa kuwa kila tafsiri inasikika kwa mtiririko, uzushi mdogo na vipimo potofu vinachanganyika na nadharia halisi. Walimu wananukuu muhtasari bila kufungua nakala asilia.',
        transcript: 'Muhtasari mlinganifu unaficha uzi uliokatika usioelekea popote.'
      },
      weight: {
        question: 'Wakati ufasaha unaficha makosa kwa urahisi, jamii inashikiliaje ukweli?',
        transcript: 'Wasomaji wawili wanaandika pambizoni na kufuatilia nukuu kati ya vitabu vitatu.',
        options: [
          { id: 'a', text: 'Lazimisha kila dai la kiotomatiki liunganishwe na shahidi mkuu asilia.' },
          { id: 'b', text: 'Tunza mijadala ya wazi (munazara) kati ya shule na lugha mbalimbali.' },
          { id: 'c', text: 'Weka nakala asilia hadharani ili yeyote popote aweze kukagua nukuu.' }
        ]
      },
      way: {
        text: 'Wasomi wa Bayt al-Hikma waliunganisha tafsiri na kinga pacha: mnyororo bayana wa upokezi (*isnad*) na maelezo ya pembeni (*hashiya*) kuonyesha wapi hakika huishia na tafsiri huanza.',
        actionCardTitle: 'Fuata madai mawili hadi ukurasa wake asilia',
        actionCardStep: 'Wakati mwingine msaidizi wa AI anapotoa muhtasari wa historia au tiba, fungua vyanzo vikuu viwili kabla ya kurudia.',
        pledgeLabel: 'Nitafuata mnyororo wa chanzo kabla ya kuamini',
        transcript: 'Maelezo ya wino pembeni yanaunganisha ukurasa wa sasa na hati asilia.'
      },
      realityMeter: {
        reason: 'Muhtasari wa haraka upo leo; vyanzo vya kubuni vinafanya uhakiki wa mtu uwe muhimu.'
      }
    },
    'west-africa-timbuktu-keepers': {
      originRegion: 'Afrika Magharibi na Sahel',
      traditionLabel: 'Maktaba za Familia za Timbuktu',
      chipTitle: 'Kuweka kidijitali hifadhi hai bila kupoteza umiliki wa wenyeji',
      title: 'Walinzi wa Timbuktu: tunza urithi bila kufungia familia nje',
      summary: 'Kila muswada dhaifu unasomwa kidijitali usiku kucha — kisha masharti yanawafungia warithi nje ya hazina yao.',
      honestyNote: 'Uskanaji wa kasi upo leo; umiliki wa haki wa jamii ndio huamua nani atamiliki kesho.',
      dependencyLabel: 'Umiliki wa taasisi za mtaa na uhuru wa lugha juu ya hifadhi',
      doorTitle: 'Utamaduni na Ubunifu',
      reviewer: 'Wazi kwa mapitio ya hifadhi za Afrika Magharibi',
      wonder: {
        text: 'Toto anafuta vumbi, anapiga picha na kuweka faharasa ya mamia ya maelfu ya vitabu vya falaki, sheria na mashairi bila kuvunja gamba hata moja.',
        totoLine: 'Toto: Kila ukurasa unang’aa alfajiri.',
        transcript: 'Mwanga wa dhahabu uanguka juu ya miswada ya ngozi uani pa maktaba tulivu.'
      },
      wobble: {
        text: 'Kampuni ya nje inapoweka hifadhi chini ya ada ya usajili, wasomi wa mtaa wanapata vitabu vya mababu nyuma ya kuta za malipo bila nakala za nje ya mtandao.',
        transcript: 'Masanduku ya kidijitali yaliyofungwa yanaelea mbali na rafu tupu za mtaa.'
      },
      weight: {
        question: 'Nani anashika funguo wakati kumbukumbu ya jamii inapokutana na kidijitali duniani?',
        transcript: 'Walinzi wanashika masanduku ya mbao pamoja na hifadhi za mtaa zilizo wazi.',
        options: [
          { id: 'a', text: 'Acha nakala mama na haki za matumizi mikononi mwa jamii husika.' },
          { id: 'b', text: 'Sambaza nakala pacha kati ya maktaba huru, kamwe si katika ghala moja.' },
          { id: 'c', text: 'Uliza wazee kurasa zipi ni za umma na zipi zinabaki amana ya familia.' }
        ]
      },
      way: {
        text: 'Familia za Timbuktu ziliokoa karne za elimu si katika jumba moja dhaifu, bali katika mamia ya masanduku ya nyumbani — kielelezo cha milele cha nakala zilizotawanywa mikononi mwa jamii.',
        actionCardTitle: 'Hifadhi kisa kimoja cha familia au sauti nje ya mtandao',
        actionCardStep: 'Hifadhi daftari la familia, pishi la asili au sauti ya mzee kwenye diski isiyo mtandaoni na mpe ndugu nakala.',
        pledgeLabel: 'Nitahifadhi kumbukumbu mikononi mwa jamii',
        transcript: 'Masanduku ya mbao na kadi za kumbukumbu zinang’aa kati ya nyumba za jirani.'
      },
      realityMeter: {
        reason: 'Uskanaji unaenda kasi leo; leseni za haki na nakala za nje ya mtandao ni muhimu.'
      }
    },
    'andean-water-terraces': {
      originRegion: 'Nyanda za Juu za Andes',
      traditionLabel: 'Andenes na Amunas za Ushirika',
      chipTitle: 'Kushirikiana maji ya milima katika misimu yote',
      title: 'Andenes na amunas: matuta yasiyoacha vijiji na kiu',
      summary: 'Umwagiliaji wa kisasa huongeza mazao ya kuuza — hadi chemchemi zinapokauka juu ya miji ya milimani.',
      honestyNote: 'Mifumo ya udongo husaidia leo; uimara wa kudumu hutegemea zamu za maji za kijiji na mifereji ya mawe.',
      dependencyLabel: 'Uhifadhi wa maji ardhini pampu za umeme zikikwama',
      doorTitle: 'Manufaa ya Umma',
      reviewer: 'Wazi kwa mapitio ya jamii za Andes',
      wonder: {
        text: 'Kwenye miteremko ya jua, Toto anasawazisha mitego ya ukungu na vali katika mamia ya matuta ya mawe. Mazao yanaiva sawia hata msimu mfupi wa barafu.',
        totoLine: 'Toto: Kila ngazi ya kijani hushika umande.',
        transcript: 'Matuta ya kijani yaliyopinda yanakumbatia vilele vya theluji wakati wa kuchomoza jua.'
      },
      wobble: {
        text: 'Kilimo cha kiotomatiki kinapotoa kipaumbele kwa mabonde ya chini yenye mtandao mkali, mifereji ya mawe (*amunas*) juu hupuuzwa — na malisho hukauka vihisi vikizimika.',
        transcript: 'Mifereji ya mawe juu inakauka huku pampu zikimulika chini bondeni.'
      },
      weight: {
        question: 'Nini hudumisha mavuno ya milimani iwe gridi inafanya kazi au imetulia?',
        transcript: 'Majirani wanatembea pamoja kukagua malango ya mawe na zana za mbao.',
        options: [
          { id: 'a', text: 'Fufua mifereji ya mawe (amunas) ili chemchemi ziendelee wiki kadhaa baada ya mvua.' },
          { id: 'b', text: 'Linda ratiba ya pamoja ya zamu za maji (ayni) kati ya juu na chini.' },
          { id: 'c', text: 'Kamwe usiweke lango la kiotomatiki bila mlango rahisi wa mbao au chuma wa mkono.' }
        ]
      },
      way: {
        text: 'Mifereji ya kale ya *amunas* bado inawafundisha wataalamu: kuelekeza maji ya mvua kwenye miamba yenye matundu hulisha chemchemi chini miezi baadaye bila umeme.',
        actionCardTitle: 'Weka akiba ya nyumbani isiyohitaji umeme',
        actionCardStep: 'Tunza maji safi ya kunywa ya siku tatu na chujio rahisi la mvuto lisilohitaji pampu.',
        pledgeLabel: 'Nitadumisha uhifadhi tulivu bila umeme',
        transcript: 'Maji safi hulisha matuta ya kijani chini ya vilele angavu.'
      },
      realityMeter: {
        reason: 'Umwagiliaji mahiri upo leo; ujazaji maji ardhini na usimamizi wa jamii huokoa ukame.'
      }
    },
    'japan-craft-repair': {
      originRegion: 'Japani',
      traditionLabel: 'Monozukuri na Sanaa ya Ukarabati',
      chipTitle: 'Kuunda chombo chochote bila kupoteza ujuzi wa kutengeneza',
      title: 'Mfuko wa Monozukuri: vifaa ambavyo yeyote anaweza kufungua na kurekebisha',
      summary: 'Kila kifaa hufika kipya alfajiri — hadi hitilafu ya umeme inapoacha makasha yaliyofungwa ambayo hakuna awezaye kuyafungua.',
      honestyNote: 'Kuunda vitu papo hapo ni hadithi; vifaa vilivyofungwa tayari vinahoji haki ya ukarabati leo.',
      dependencyLabel: 'Saa ambazo jamii huendelea vyema usambazaji na vipuri vikisimama',
      doorTitle: 'Teknolojia za Kila Siku',
      reviewer: 'Wazi kwa mapitio ya mafundi wa Japani na uhandisi',
      wonder: {
        text: 'Sufuria iliyopasuka au mnyororo uliokatika — Toto anakupa kipya kwa pumzi moja. Miji inaenda safi bila takataka.',
        totoLine: 'Toto: Chochote kilichovunjika kimebadilishwa.',
        transcript: 'Vifaa vinavyong’aa juu ya meza safi ya seremala katika mwanga wa asubuhi.'
      },
      wobble: {
        text: 'Baada ya miaka ya ubadilishaji uliofungwa, maduka ya vifaa na mafundi wa mtaa hufunga. Tetemeko likikata nyaya za bandari, nyumba hubaki na vifaa visivyo na skrubu wala mchoro.',
        transcript: 'Mashine laini zisizo na skrubu zinasimama mbele ya rafu tupu.'
      },
      weight: {
        question: 'Mashine zinapobadilisha kila kitu kirahisi, ni ujuzi gani unashikilia mji imara?',
        transcript: 'Mafundi wanarekebisha kiungo cha mbao kando ya kipuri cha kisasa.',
        options: [
          { id: 'a', text: 'Lazimisha skrubu za kawaida, michoro iliyochapishwa na haki halisi ya kutengeneza.' },
          { id: 'b', text: 'Weka karakana za mtaa na mafunzo ya uanagenzi hai katikati ya uotomatishaji.' },
          { id: 'c', text: 'Fungua vipuri kwa mafundi huru badala ya kampuni moja pekee.' }
        ]
      },
      way: {
        text: 'Kutoka uunganishaji mbao bila gundi (*kigumi*) hadi ukarabati wa dhahabu (*kintsugi*), ufundi bora huona uwezo wa kutengenezwa kama uzuri — kupitia vipuri vinavyofunguka na sanduku dogo la vifaa nyumbani.',
        actionCardTitle: 'Weka kifaa kimoja cha mkono na mchoro wa karatasi',
        actionCardStep: 'Jifunze kufunga bomba kuu la maji na swichi kuu ya umeme kwa mkono, na weka bisibisi za kawaida.',
        pledgeLabel: 'Nitatunza ujuzi wa msingi wa ukarabati wa mikono',
        transcript: 'Nyufa zilizorekebishwa kwa dhahabu zinang’aa kando ya zana za karakana.'
      },
      realityMeter: {
        reason: 'Viundaji vya papo hapo ni hadithi; vifaa vilivyofungwa tayari vinapinga haki ya kukarabati.'
      }
    },
    'nordic-right-to-roam': {
      originRegion: 'Ushirika wa Nchi za Nordic',
      traditionLabel: 'Allemansrätten na Vyanzo Wazi vya Umma',
      chipTitle: 'Kuacha nyenzo za pamoja wazi kazi zinapofanywa na mashine',
      title: 'Njia wazi katika dunia ya kasi: huduma bila vizuizi vya siri',
      summary: 'Wasaidizi hurahisisha kila kazi — hadi huduma za umma na kipato zinapohamia ndani ya malango ya kulipia.',
      honestyNote: 'Uotomatishaji wa ofisi tayari unapunguza kazi za kawaida; kanuni wazi na kinga ya kijamii huamua usawa.',
      dependencyLabel: 'Kinga ya mapato na mafunzo upya pale kazi za kawaida zinapobadilika',
      doorTitle: 'Teknolojia za Kila Siku',
      reviewer: 'Wazi kwa mapitio ya sera ya umma ya Nordic',
      wonder: {
        text: 'Manispaa zinaunganisha wasaidizi wepesi na afya ya umma, usafiri na uhuru wa kufikia misitu na ghuba.',
        totoLine: 'Toto: Kila shughuli imemalizika kabla ya kifungua kinywa.',
        transcript: 'Kibao cha njia ya mbao kinaelekeza misituni kando ya kituo tulivu cha tramu.'
      },
      wobble: {
        text: 'Ndani ya misimu miwili, majukwaa ya leseni yanatawala huduma za mji na kazi za ofisi — yakitoza kila swali huku mishahara na bajeti za mafunzo zikibaki nyuma.',
        transcript: 'Vizuizi vya kulipia vinaibuka juu ya njia kati ya nyumba, ofisi na ukumbi.'
      },
      weight: {
        question: 'Uotomatishaji unapoharakisha kazi za kawaida, nini humwacha kila mkazi huru kusonga?',
        transcript: 'Wananchi wanakagua viwango wazi na pasi za kujifunza maishani.',
        options: [
          { id: 'a', text: 'Unganisha faida ya tija na kinga ya mapato pamoja na mafunzo endelevu.' },
          { id: 'b', text: 'Weka huduma za kidijitali za umma kwa viwango wazi bila ukiritimba wa kampuni.' },
          { id: 'c', text: 'Linda haki ya kisheria ya huduma za ana kwa ana zisizohitaji skrini.' }
        ]
      },
      way: {
        text: 'Haki ya *Allemansrätten* ya Nordic huhakikisha njia wazi maadamu unatunza ardhi — dira ya wazi kwa AI ya umma yenye itifaki wazi na kinga imara.',
        actionCardTitle: 'Hakikisha huduma za mtaa zinabakiza mlango wazi',
        actionCardStep: 'Thibitisha kuwa baraza lako, benki au kliniki zinahifadhi huduma ya moja kwa moja au simu kando ya programu.',
        pledgeLabel: 'Nitalinda ufikiaji wazi wa huduma za raia',
        transcript: 'Njia wazi za misonobari zinaendelea kando ya viti mbele ya maji tulivu.'
      },
      realityMeter: {
        reason: 'Mabadiliko ya kazi za akili yanaendelea; viwango wazi na kinga za kijamii hudumisha utulivu.'
      }
    },
    'anatolia-mediterranean-crossroads': {
      originRegion: 'Mediterania Mashariki na Anatolia',
      traditionLabel: 'Njia Panda za Mawe na Viwanja vya Umma',
      chipTitle: 'Kuviacha viwanja vya jamii vitulivu wakati wa majanga',
      title: 'Njia panda za mawe: miji ya kidijitali inayoheshimu ardhi na majirani',
      summary: 'Skrini za mji hupanga feri na viwanja — hadi mitikisiko ya ardhi inapozima minara ya simu mitaani.',
      honestyNote: 'Miji pacha ya kidijitali inatumika leo; uimara wa majengo na sehemu za kukutana nje ya mtandao ndizo huamua.',
      dependencyLabel: 'Ustahimilivu wa umeme na utayari wa kukutana mitaani katika miji ya kale',
      doorTitle: 'Utamaduni na Ubunifu',
      reviewer: 'Wazi kwa mapitio ya Mediterania na jamii',
      wonder: {
        text: 'Kutoka Bosphorus hadi Aegean, Toto husawazisha feri za asubuhi, vihisi vya kuta za mawe na vivuli ili mitaa ibaki tulivu kwa wazee na mafundi.',
        totoLine: 'Toto: Feri, tramu na viwanja vinatiririka pamoja.',
        transcript: 'Feri nyeupe zinateleza juu ya maji tulivu mbele ya matao ya mawe na misonobari.'
      },
      wobble: {
        text: 'Kutegemea vihisi vya wingu kulizaa utulivu bandia: mbao za matangazo na mazoezi yalipunguzwa — na familia zikachanganyikiwa mtandao ulipoanguka.',
        transcript: 'Simu zilizonyamaza zinamulika kando ya skrini zilizozimwa na chemchemi kimya.'
      },
      weight: {
        question: 'Mitandao ya mji ikizima kwenye dhoruba au tetemeko, nini huwakutanisha majirani haraka zaidi?',
        transcript: 'Majirani wanakusanyika kando ya birika la umma na ubao wa chaki wa mtaa.',
        options: [
          { id: 'a', text: 'Tunza viwanja wazi visivyohitaji umeme, visima na ramani za karatasi kila kata.' },
          { id: 'b', text: 'Wekeza kwanza katika kuimarisha majengo halisi kabla ya skrini za kisasa.' },
          { id: 'c', text: 'Wafundishe wenye maduka na viongozi wa mtaa kuratibu ukaguzi wa jirani.' }
        ]
      },
      way: {
        text: 'Kwa karne nyingi katika Mediterania, mitaa ilivuka mitikisiko kupitia viwanja wazi, hifadhi za maji za mvuto na mshikamano wa ujirani — muundo hai ambao hitilafu ya programu haiwezi kuuzima.',
        actionCardTitle: 'Fahamu uwanja wazi wa kukutana wa mtaa wako',
        actionCardStep: 'Kubaliana na familia kuhusu bustani au uwanja mmoja ndani ya mwendo wa dakika kumi ambapo mtakutana simu zikizima.',
        pledgeLabel: 'Najua uwanja wetu wa kukutana bila mtandao',
        transcript: 'Mizeituni inazunguka uwanja wenye jua, mabomba ya maji na vibao vilivyo wazi.'
      },
      realityMeter: {
        reason: 'Uongozaji wa miji upo leo; uimara wa majengo na mikusanyiko ya ana kwa ana hubaki kipaumbele.'
      }
    }
  }
};

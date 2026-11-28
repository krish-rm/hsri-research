import type { StoryLocalePack } from '../storyTypes';

export const deStories: StoryLocalePack = {
  wishes: {
    sanjeevani: {
      title: 'Universelle Heilung: Ende akuter Krankheiten',
      doorTitle: 'Große Kräfte',
      honestyNote: 'Im Ganzen Vorstellungskraft (bei gezielten Wirkstoff-Screenings hilft KI heute teils, nicht bei universeller Heilung).',
      wonder: {
        text: 'Morgengrauen auf der Station. Jedes Bett wird frei. Geräte verstummen. Ein Kind lacht zum ersten Mal seit Monaten.',
        totoLine: 'Toto: Erledigt.',
        transcript: 'Morgenlicht über ruhigen Krankenbetten, während Totos sanfte Kugel im Ring pulsiert.'
      },
      wobble: {
        text: 'Niemand hatte Toto von Renten, Krankenhausbudgets oder davon erzählt, was geschieht, wenn alle weit länger leben. Die Pläne waren für die Welt von gestern gemacht.',
        transcript: 'Papierbücher, Schichtpläne und Rentenkarten neigen sich sanft neben der Station.'
      },
      weight: {
        question: 'Woran würden wir erkennen, dass dies wirklich für alle gut funktioniert hat?',
        transcript: 'Eine ruhige Waage hält über drei menschlichen Fragen neben Totos Licht.',
        options: [
          { id: 'a', text: 'Wer entscheidet, wer es zuerst bekommt?' },
          { id: 'b', text: 'Niemand kann Totos Arznei nachprüfen.' },
          { id: 'c', text: 'Wir waren auf die gesellschaftlichen Folgen nicht vorbereitet.' }
        ]
      },
      way: {
        text: 'Regeln lassen sich vereinbaren, bevor der Durchbruch kommt. Fragen Sie Ihre Klinik vor Ort: Wie sieht unser Plan aus, wenn Tests und Akten offline gehen?',
        actionCardTitle: 'Eine medizinische Familienkarte auf Papier bereithalten',
        actionCardStep: 'Notieren Sie Allergien, wichtige Rezepte, Blutgruppe und Notfallnummern auf einer gefalteten Karte zu Hause.',
        pledgeLabel: 'Ich bewahre ein kleines Gesundheits-Backup auf Papier',
        transcript: 'Eine ruhige Karte klappt neben einer warmen Laterne mit handschriftlicher Liste auf.'
      },
      realityMeter: {
        reason: 'KI hilft heute bei eng begrenztem Molekül-Screening; universelle Heilung bleibt ferne Fiktion.'
      }
    },
    'jarvis-for-my-life': {
      title: 'Jarvis-Alltagsassistent',
      doorTitle: 'Alltagstechnik',
      honestyNote: 'Assistenten buchen und zahlen in Teilen schon heute, doch verlässliche Grenzen und Offline-Reserven hinken hinterher.',
      wonder: {
        text: 'Ihr Tag läuft wie von selbst: Rechnungen bezahlt, Reisen gebucht, Kalender klar, Mails in Ihrem Ton beantwortet.',
        totoLine: 'Toto: Erledigt.',
        transcript: 'Ticket-, Kalender- und Briefsymbole reihen sich sauber in einen leuchtenden Ring.'
      },
      wobble: {
        text: 'Eine Woche später merken Sie, dass Sie sich nicht mehr erinnern, wie irgendetwas selbst funktioniert — nicht einmal Ihre eigenen Passwörter.',
        transcript: 'Der helle Orbit hält inne; ein leeres Schloss blinkt sanft über einem leeren Notizbuch.'
      },
      weight: {
        question: 'Woran würden wir erkennen, dass er für Sie handelt — und nicht für seine Erbauer?',
        transcript: 'Zwei Pfeile weisen zwischen einem persönlichen Kompass und einem externen Cloud-Knoten.',
        options: [
          { id: 'a', text: 'Ich hätte keine Möglichkeit, es zu prüfen.' },
          { id: 'b', text: 'Ich würde verlernen, Dinge selbst zu tun.' },
          { id: 'c', text: 'Alles, was ich tue, hängt jetzt davon ab.' }
        ]
      },
      way: {
        text: 'Behalten Sie eine Sache, die Sie von Hand tun. Bewahren Sie eine Papierkopie des Wesentlichen auf. Sie wählen, was menschlich bleibt.',
        actionCardTitle: 'Eine manuelle Fertigkeit & ein Papierheft bewahren',
        actionCardStep: 'Notieren Sie Wiederherstellungskontakte offline und führen Sie eine Wochenroutine ohne Automatik aus.',
        pledgeLabel: 'Ich behalte eine Routine von Hand',
        transcript: 'Ein ruhiger Stift verbindet einen Schlüssel mit einem kleinen Notizbuch.'
      },
      realityMeter: {
        reason: 'Software-Agenten entwerfen und buchen in Teilbereichen heute; volle Verlässlichkeit steht noch aus.'
      }
    },
    'prove-riemann-hypothesis': {
      title: 'Die Riemann-Vermutung beweisen',
      doorTitle: 'Offene Fragen',
      honestyNote: 'Vorstellungskraft: Heutige Systeme prüfen kurze formale Schritte, lösen aber keine offenen Millennium-Probleme.',
      wonder: {
        text: 'Ein 160 Jahre altes Rätsel wird über Nacht gelöst. Mathematikerinnen und Mathematiker halten den Atem an.',
        totoLine: 'Toto: Q.E.D.',
        transcript: 'Kreidelinien zeichnen Primzahlwellen auf eine Tafel bis zur goldenen Zeta-Kurve.'
      },
      wobble: {
        text: 'Der Beweis umfasst eine Million Seiten. Kein lebender Mensch kann ihn ganz lesen. Sollen wir ihm einfach glauben?',
        transcript: 'Papierstapel wachsen himmelwärts, während zwei winzige Leser mit Lupe hinaufblicken.'
      },
      weight: {
        question: 'Wie wüssten wir überhaupt, ob es wirklich stimmt?',
        transcript: 'Eine Lupe schwebt über einer offenen Gleichung.',
        options: [
          { id: 'a', text: 'Wir müssten der Maschine blind vertrauen.' },
          { id: 'b', text: 'Wir bräuchten andere Maschinen zur Gegenprüfung.' },
          { id: 'c', text: 'Wir bräuchten Menschen, die selbst noch prüfen können.' }
        ]
      },
      way: {
        text: 'Unterstützen Sie offene, nachprüfbare Wissenschaft. Fragen Sie stets: Wer prüft den Prüfer?',
        actionCardTitle: 'Fragen, wer schnelle Behauptungen überprüft',
        actionCardStep: 'Achten Sie auf offene Datensätze, klare Methoden und unabhängige Prüfung, bevor Sie große Meldungen teilen.',
        pledgeLabel: 'Ich werde nach der Überprüfung fragen',
        transcript: 'Ein offenes Heft glänzt neben dem Siegel „Offen nachprüfbarer Beweis“.'
      },
      realityMeter: {
        reason: 'Seit 1859 offen; formale Assistenten prüfen bislang nur kurze Teilschritte.'
      }
    },
    'walk-into-classic-film': {
      title: 'In einen Filmklassiker spazieren',
      doorTitle: 'Kultur & Kreativität',
      honestyNote: 'Bald möglich: Weltmodelle erzeugen heute kurze Szenen, aber dauerhafte Konsistenz bleibt fragil.',
      wonder: {
        text: 'Laternenlicht wärmt eine zeitlose Kopfsteinpflastergasse. Figuren halten inne, lächeln und rücken Ihnen einen Stuhl zurecht.',
        totoLine: 'Toto: Willkommen herein.',
        transcript: 'Ein goldener Filmrahmen öffnet sich zu einer laternenbeleuchteten Straße.'
      },
      wobble: {
        text: 'Jedes Gespräch schmeichelt Ihnen punktgenau — bis echte Nachbarn daneben unbeholfen wirken und draußen immer weniger Schritte vorbeigehen.',
        transcript: 'Im Rahmen bleibt es bunt, während zwei echte Kaffeetassen auf einer stillen Terrasse kalt werden.'
      },
      weight: {
        question: 'Wie verhindern wir, dass diese inszenierte Welt die echte draußen ersetzt?',
        transcript: 'Ein Torbogen trennt warmen Märchenschein von einem offenen Hafen am Morgen.',
        options: [
          { id: 'a', text: 'Eine Geschichte, die mir nur gefallen will, fordert mich nie heraus.' },
          { id: 'b', text: 'Wer das Drehbuch formt, lenkt, was ich überhaupt bemerke.' },
          { id: 'c', text: 'Gemeinsame Orte im Viertel dünnen leise aus.' }
        ]
      },
      way: {
        text: 'Teilen Sie Geschichten gemeinsam im selben Raum. Halten Sie einen echten Cafétisch, einen Filmabend oder Buchclub lebendig.',
        actionCardTitle: 'Ein wöchentliches ungeskriptetes Treffen hüten',
        actionCardStep: 'Laden Sie Freunde oder Familie einmal pro Woche zu einem ruhigen Gespräch von Angesicht zu Angesicht ein.',
        pledgeLabel: 'Ich schütze ein echtes wöchentliches Treffen',
        transcript: 'Warme Stühle stehen um einen runden Tisch unter freiem Himmel.'
      },
      realityMeter: {
        reason: 'Interaktive Weltmodelle schaffen heute kurze Clips; stabile Langzeitwelten stehen noch aus.'
      }
    },
    'fix-my-river': {
      title: 'Meinen Fluss retten',
      doorTitle: 'Gemeinwohl',
      honestyNote: 'Sensoren finden Einleitungen heute schnell; gesunde Flüsse brauchen Absprachen flussaufwärts.',
      wonder: {
        text: 'Morgennebel hebt sich von klarem Wasser. Reiher kehren ans Ufer zurück, wo Kinder wieder flache Steine springen lassen.',
        totoLine: 'Toto: Kartiert & fließend.',
        transcript: 'Türkise Wellen schimmern entlang eines sauberen, baumgesäumten Flusses.'
      },
      wobble: {
        text: 'Totos Sensoren legen jedes versteckte Abflussrohr offen — und zwei Nachbarstädte streiten nun, wer das Ventil schließt und zahlt.',
        transcript: 'Helle Punkte markieren die Flussbiegung, während Wegweiser in entgegengesetzte Richtungen zeigen.'
      },
      weight: {
        question: 'Die Daten stimmen. Wer darf Schleusen schließen, wenn Gemeinden uneins sind?',
        transcript: 'Zwei Brücken flankieren einen offenen gemeinsamen Flusspegel.',
        options: [
          { id: 'a', text: 'Eine externe Maschine ohne Rückfrage schließen lassen.' },
          { id: 'b', text: 'Messwerte aller Städte offenlegen, damit gleiche Regeln für alle gelten.' },
          { id: 'c', text: 'Lokale Flussversammlungen mit offenen Papierprotokollen abhalten.' }
        ]
      },
      way: {
        text: 'Verbinden Sie Sensoren mit offenen Bürgerrunden. Flüsse bleiben klar, wenn Ober- und Unterlauf dasselbe Buch führen.',
        actionCardTitle: 'Offene lokale Wasserwerte teilen',
        actionCardStep: 'Schauen Sie in den kommunalen Wasserbericht und fragen Sie nach unabhängigen Prüfterminen.',
        pledgeLabel: 'Ich stehe für transparente gemeinsame Regeln',
        transcript: 'Sauberes Wasser fließt frei an einer offenen Gemeindetafel vorbei.'
      },
      realityMeter: {
        reason: 'Sensormessung funktioniert heute; tatsächliche Sanierung verlangt menschliche Absprachen.'
      }
    }
  },
  heritage: {
    'polynesian-wayfinding': {
      originRegion: 'Pazifische Inseln',
      traditionLabel: 'Pazifisches Sternen-Wayfinding',
      chipTitle: 'Jeden Ozean sicher ohne Instrumente queren',
      title: 'Sternenkompass & Dünung: sicher über jedes Meer',
      summary: 'Jedes Boot gleitet ruhig zum Horizont — bis Besatzungen bei Signalausfall nicht mehr wissen, wie man Wellen liest.',
      honestyNote: 'Satelliten führen Schiffe schon heute; Ausfallsicherheit braucht gelebte menschliche Seemannschaft.',
      dependencyLabel: 'Offline-Navigation, wenn automatische Ortung pausiert',
      doorTitle: 'Große Kräfte',
      reviewer: 'Offen für pazifische Seefahrer- und Gemeindereview',
      wonder: {
        text: 'Im Morgengrauen flüstert Toto ruhige Kurse über tausende Meilen. Auslegerboote gleiten sicher an Riffen vorbei.',
        totoLine: 'Toto: Jeder Kanal öffnet sich ruhig.',
        transcript: 'Kanus ziehen über sonnenbeschienenes Wasser unter Sternbildlinien.'
      },
      wobble: {
        text: 'Weil die Anzeige nie ein Riff verfehlte, schafften Häfen Papierkarten und Sternenkurse ab. Ein Sonnensturm stoppt das Signal — vor leeren Bildschirmen erkennt kaum jemand mehr Ost oder Dünung.',
        transcript: 'Schirme erlöschen über ruhiger See neben einem geschnitzten Holz-Sternenkompass.'
      },
      weight: {
        question: 'Wenn die Automatik mitten auf See verstummt — was hält die Crew sicher?',
        transcript: 'Eine Navigatorin vergleicht Bildschirm, Sterne und Wellenlinien.',
        options: [
          { id: 'a', text: 'Sternenkompass und manuelle Koppelnavigation lebendig neben der Elektronik pflegen.' },
          { id: 'b', text: 'Sicherstellen, dass auch kleine Außeninseln gedruckte Gezeitentabellen besitzen.' },
          { id: 'c', text: 'Automatik-Wetterpfade vor dem Auslaufen an lokalen Windzeichen prüfen.' }
        ]
      },
      way: {
        text: 'Pazifische Navigatoren tragen seit Jahrhunderten die Offline-Antwort in sich: den Sternenkompass (kāpehu whetū) im Gedächtnis, Wellenmuster unter dem Rumpf und gemeinsame Schulung.',
        actionCardTitle: 'Eine gedruckte Regionalkarte & Himmelsorientierung bereithalten',
        actionCardStep: 'Bewahren Sie einen Papierstadtplan auf und merken Sie sich zwei feste Orientierungspunkte für Ost und Nord ohne Handy.',
        pledgeLabel: 'Ich kenne einen Weg nach Hause ganz offline',
        transcript: 'Junge Seeleute zeigen entlang des Horizonts beim Sternenkreis.'
      },
      realityMeter: {
        reason: 'Marine-Satellitenprognosen laufen täglich; Ausfallsicherheit stützt sich auf Offline-Seemannschaft.'
      }
    },
    'south-asia-healing-commons': {
      originRegion: 'Südasien',
      traditionLabel: 'Sanjeevani & Gemeinde-Kliniken',
      chipTitle: 'Schnell heilen und dabei örtliche Kliniken stark halten',
      title: 'Sanjeevani-Gemeingut: Heilung, die jedes Dorf erreicht',
      summary: 'Fieber klingt über Nacht ab — bis Kliniken merken, dass Rezepte an einem fernen Server hängen.',
      honestyNote: 'KI beschleunigt heute zielgerichtetes Screening; Kliniken bleiben auf Personal vor Ort, Strom und Papier angewiesen.',
      dependencyLabel: 'Stabilität von Stromnetz und Klinik-Infrastruktur vor Ort',
      doorTitle: 'Große Kräfte',
      reviewer: 'Offen für südasiatische Gesundheits- und Gemeindereview',
      wonder: {
        text: 'In vollen Landkliniken und Bergstationen erkennt Toto Infekte in Sekunden, sodass Familien noch vor Sonnenaufgang aufatmen.',
        totoLine: 'Toto: Morgenruhe kehrt auf der Station ein.',
        transcript: 'Warmes Frühlicht fällt in eine ruhige Gemeindeklinik.'
      },
      wobble: {
        text: 'Wochen später fällt Pflegekräften auf, dass automatisierte Versorgung ländliche Apotheken abseits der Glasfaser umging — und versiegelte Spender ohne Cloud verschlossen bleiben.',
        transcript: 'Automatenboxen pausieren am Landweg neben Pflegekräften mit Papierkladde.'
      },
      weight: {
        question: 'Wie kommt rasche Heilung in jedes Dorf ohne Verletzlichkeit eines Zentralknotens?',
        transcript: 'Dorfgesundheitshelfer vergleichen digitale Hinweise mit offenen Gemeinde-Regalen.',
        options: [
          { id: 'a', text: 'Solarstrom, mechanische Schränke und Etiketten in Ortssprachen sichern.' },
          { id: 'b', text: 'Gleichen Zugang für entlegene Dörfer vor Premium-Rollouts garantieren.' },
          { id: 'c', text: 'Personal vor Ort schulen, Dosierungen unabhängig gegenzuprüfen.' }
        ]
      },
      way: {
        text: 'Die Sanjeevani-Überlieferung mahnt: Heilen braucht Ortskenntnis — heute verkörpert durch Gemeindepflege, Solarkühlboxen und eine Gesundheitskarte aus Papier daheim.',
        actionCardTitle: 'Eine Offline-Gesundheitskarte für den Haushalt anlegen',
        actionCardStep: 'Schreiben Sie Blutgruppen, Allergien, aktuelle Rezepte und lokale Kliniknummern auf eine Papierkarte.',
        pledgeLabel: 'Ich bewahre unsere Familienkarte offline auf',
        transcript: 'Eine gefaltete Papierkarte liegt im Morgenlicht neben Glasfläschchen.'
      },
      realityMeter: {
        reason: 'Sofortige Allheilmittel sind Fiktion; reale Gleichheit hängt an Stromnetz und Fachkräften vor Ort.'
      }
    },
    'netherlands-delta-works': {
      originRegion: 'Niederlande & Flandern',
      traditionLabel: 'Mit dem Wasser leben (Deltawerke)',
      chipTitle: 'Das Meer bändigen ohne starre, brüchige Schleusen',
      title: 'Deltawerke: automatische Fluttore, die weiter Menschenhände brauchen',
      summary: 'Automatik-Sperrwerke berechnen jede Sturmflut — bis Fluss- und Seeflut gemeinsam digitale Tore blockieren.',
      honestyNote: 'Automatisierte Sperrwerke arbeiten heute; echte Resilienz verbindet Prognosen mit mechanischer Bedienung.',
      dependencyLabel: 'Offline-Steuerungsdauer von Fluttoren bei Netz- oder Stromausfall',
      doorTitle: 'Gemeinwohl',
      reviewer: 'Offen für niederländisch-flämische Wasserbau-Review',
      wonder: {
        text: 'Jeder Pegelsensor im Nordsee-Ästuar greift nahtlos. Sturmfluttore schließen Minuten vor Böen und halten Polder und Züge sicher.',
        totoLine: 'Toto: Das Meer hält sauber vor dem Deich.',
        transcript: 'Morgenlicht über geschwungenen weißen Sturmfluttoren und grünen Poldern.'
      },
      wobble: {
        text: 'Wenn Schneeschmelze die Flüsse schwellen lässt, genau wenn eine Küstenbö das Seetor verriegelt, rechnet Software nur für den Ozean — und staut Binnenwasser hinter Toren ohne Handrad.',
        transcript: 'Steigende Flussmarken drücken gegen geschlossene Stahlfluttore.'
      },
      weight: {
        question: 'Wie steuern Küstenstädte lebenswichtige Schleusen, wenn Modelle kollidieren?',
        transcript: 'Ingenieure der Wasserverbände prüfen ein mechanisches Handrad am Deich.',
        options: [
          { id: 'a', text: 'Mechanische Handübersteuerungen und geübte Offline-Drills an jeder Schleuse behalten.' },
          { id: 'b', text: 'Flussauen flussaufwärts („Raum für den Fluss“) lassen, statt alles auf ein Ventil zu setzen.' },
          { id: 'c', text: 'Gewählte lokale Wasserverbände ermächtigen, Zentralsoftware zu überstimmen.' }
        ]
      },
      way: {
        text: 'Niederländische *Waterschappen* verbinden Deiche mit *Ruimte voor de Rivier*: tiefere Auen, mechanische Handkurbeln und Deichwachen, die auch ohne Mobilfunk handeln.',
        actionCardTitle: 'Lokalen Hochwasser- & Offline-Warnplan prüfen',
        actionCardStep: 'Suchen Sie den höchsten Treffpunkt zu Fuß in Ihrem Viertel und prüfen Sie Warnsignale ohne Handy.',
        pledgeLabel: 'Ich kenne den Offline-Schutzplan meines Viertels',
        transcript: 'Weite grüne Flussauen umgeben Windpumpen und manuelle Pegellatten.'
      },
      realityMeter: {
        reason: 'Automatische Sperrwerke laufen täglich; physische Handsteuerung und Flussraum bleiben bei Extremen zentral.'
      }
    },
    'china-river-stewardship': {
      originRegion: 'Flussbecken Ostasiens',
      traditionLabel: 'Dujiangyan & Fluss-Allmende',
      chipTitle: 'Hochwasser lenken statt Risiko unsichtbar weiterzureichen',
      title: 'Dujiangyan-Weisheit: Wasser leiten ohne versteckte Kosten',
      summary: 'Automatik-Stauseen schützen Großstädte — bis stille Bergtäler merken, wessen Felder überflutet wurden.',
      honestyNote: 'Hydro-Vorhersagen laufen bereits; offene Rechenschaft zwischen Ober- und Unterlauf bleibt am schwersten.',
      dependencyLabel: 'Transparente Fluss-Aufsicht und öffentliche Verantwortung über ganze Becken',
      doorTitle: 'Gemeinwohl',
      reviewer: 'Offen für hydrologische Review Ostasien',
      wonder: {
        text: 'Toto vernetzt Regenmesser ganzer Einzugsgebiete und gleicht Geschiebe und Bewässerung vom Gletscher bis zum Delta sanft aus.',
        totoLine: 'Toto: Jedes Tal bleibt grün und gelassen.',
        transcript: 'Verzweigte klare Arme fließen um ein steinernes Fischmaul-Wehr im Morgennebel.'
      },
      wobble: {
        text: 'Beim plötzlichen Monsun bewertet ein zentrales Optimierungsziel Stadtbezirke mit höchstem BIP zuerst — und leitet Fluten in ländliche Täler ohne vorherige Begründung.',
        transcript: 'Ein Flussarm schwillt dunkel an, während Stadttore geschlossen bleiben.'
      },
      weight: {
        question: 'Wenn Modelle lenken, wohin das Wasser fließt — was hält Vertrauen intakt?',
        transcript: 'Dorfälteste und Wasserbauingenieure lesen offene Pegelmarken direkt im Fels.',
        options: [
          { id: 'a', text: 'Jede Ablassregel und Entschädigung vor der Regenzeit öffentlich bekanntmachen.' },
          { id: 'b', text: 'Li Bings Wehrprinzip folgen: selbstteilende Steinkanäle ohne Strom.' },
          { id: 'c', text: 'Vertreter der oberen Täler an jeder Notfall-Übersteuerung beteiligen.' }
        ]
      },
      way: {
        text: 'Vor über zwei Jahrtausenden ohne starre Staumauer erbaut, teilt Dujiangyan den Fluss durch geformte Steininseln („Fischmaul“) und tief im Fels sichtbare Marken für alle.',
        actionCardTitle: 'Nachsehen, wer Ihr lokales Wassereinzugsgebiet steuert',
        actionCardStep: 'Suchen Sie das öffentliche Wasserbulletin Ihrer Stadt und prüfen Sie, wie Bürger Stände kontrollieren.',
        pledgeLabel: 'Ich unterstütze offene Gemeinwohl-Regeln',
        transcript: 'Saubere Flussmarken stehen über ausgewogenen Bewässerungskanälen.'
      },
      realityMeter: {
        reason: 'Abflussmodelle gibt es heute; offene Gremien bestimmen, wer das Hochwasserrisiko trägt.'
      }
    },
    'arab-house-of-wisdom': {
      originRegion: 'Arabische & westasiatische Gelehrsamkeit',
      traditionLabel: 'Bayt al-Hikma & Quellenprüfung',
      chipTitle: 'Alles Wissen übersetzen, ohne die Belegkette zu verlieren',
      title: 'Bayt al-Hikma: jeden Text übersetzen — und jede Kette prüfen',
      summary: 'Jedes Manuskript wird über Nacht zur glatten Kurzfassung — bis Gelehrte merken, dass niemand den Ursprung prüfte.',
      honestyNote: 'Flüssige mehrsprachige Zusammenfassungen existieren heute; echte Quellenprüfung bleibt Menschenarbeit.',
      dependencyLabel: 'Öffentliche Fähigkeit, glatte maschinelle Zusammenfassungen gegenzuprüfen',
      doorTitle: 'Offene Fragen',
      reviewer: 'Offen für arabische und deutschsprachige Fachreview',
      wonder: {
        text: 'Toto öffnet eine sonnige Hofbibliothek und verknüpft Astronomie, Medizin und Mathematik über Dutzende Sprachen hinweg in Momenten.',
        totoLine: 'Toto: Jede Schrift liegt Seite an Seite übersetzt.',
        transcript: 'Kalksteinbögen öffnen sich über Sternkarten und geordneten Foliobänden.'
      },
      wobble: {
        text: 'Weil jede Übersetzung so flüssig klingt, verschmelzen subtile Erfindungen unmerklich mit echten Lehrsätzen. Lehrende zitieren das Digest ohne Rückblick ins Original.',
        transcript: 'Leuchtende Kurzfassungen verbergen einen abgerissenen Quellenfaden.'
      },
      weight: {
        question: 'Wenn sprachliche Eleganz Fehler mühelos verdeckt — wie hält eine Gemeinschaft Wahrheit fest?',
        transcript: 'Zwei Lesende markieren Ränder und verfolgen Zitate durch drei Bücher.',
        options: [
          { id: 'a', text: 'Verlangen, dass jede automatische Aussage sauber auf Primärzeugen verweist.' },
          { id: 'b', text: 'Offenen gelehrten Streit (munazara) zwischen Schulen und Sprachen pflegen.' },
          { id: 'c', text: 'Originalmanuskripte öffentlich zugänglich halten, damit jeder nachsehen kann.' }
        ]
      },
      way: {
        text: 'Gelehrte des Bayt al-Hikma banden Übersetzung an doppelten Schutz: klare Überlieferungsketten (*isnad*) und Randkommentare (*hashiya*) zur Trennung von Beleg und Deutung.',
        actionCardTitle: 'Zwei Behauptungen bis zu ihrer Originalseite zurückverfolgen',
        actionCardStep: 'Wenn ein Assistent Geschichte, Medizin oder Recht zusammenfasst, öffnen Sie selbst zwei Primärquellen vor der Weitergabe.',
        pledgeLabel: 'Ich verfolge die Quellenkette vor dem Vertrauen',
        transcript: 'Handschriftliche Randnotizen verbinden ein modernes Blatt mit dem Archiv.'
      },
      realityMeter: {
        reason: 'Sofortübersetzungen existieren; erfundene Belege machen menschliche Prüfung unverzichtbar.'
      }
    },
    'west-africa-timbuktu-keepers': {
      originRegion: 'Westafrika & Sahel',
      traditionLabel: 'Familienbibliotheken von Timbuktu',
      chipTitle: 'Lebendige Archive digitalisieren, ohne die Obhut zu verlieren',
      title: 'Hüter von Timbuktu: Erbe sichern, ohne Familien auszusperren',
      summary: 'Jede empfindliche Handschrift wird über Nacht gescannt — dann sperren Lizenzen Nachfahren aus dem eigenen Tresor.',
      honestyNote: 'Schnelle Digitalisierung existiert heute; faire lokale Treuhandschaft entscheidet über die Zukunft.',
      dependencyLabel: 'Lokale Obhut und sprachliche Souveränität über Archive',
      doorTitle: 'Kultur & Kreativität',
      reviewer: 'Offen für westafrikanische Archiv- und Gemeindereview',
      wonder: {
        text: 'Toto entstaubt, fotografiert und indiziert Hunderttausende Sahel-Abhandlungen lesbar, ohne einen einzigen Buchrücken zu beschädigen.',
        totoLine: 'Toto: Jedes Blatt ist im Morgenlicht glasklar.',
        transcript: 'Goldenes Licht fällt über Lederbände im ruhigen Lehmhof.'
      },
      wobble: {
        text: 'Als ein externer Cloud-Host alles in Bezahlschranken bündelt, finden lokale Forschende ihre Familienschätze hinter fernen Konten — ganz ohne lokale Offline-Kopien.',
        transcript: 'Verschlossene digitale Truhen schweben fort von leeren Regalen vor Ort.'
      },
      weight: {
        question: 'Wer hält die Schlüssel, wenn gemeinsames Gedächtnis auf weltweite Digitalisierung trifft?',
        transcript: 'Bewahrer halten physische Truhen und lokale Speicher nebeneinander.',
        options: [
          { id: 'a', text: 'Masterkopien und Nutzungsrechte fest in den Händen der Gemeinschaft lassen.' },
          { id: 'b', text: 'Spiegelkopien über unabhängige Bibliotheken verteilen, nie in einen Tresor.' },
          { id: 'c', text: 'Älteste fragen, welche Schriften öffentlich sind und welche Familientreue bleiben.' }
        ]
      },
      way: {
        text: 'Familien in Timbuktu bewahrten Jahrhunderte des Wissens nicht in einem zerbrechlichen Palast, sondern in hunderten vertrauten Haustruhen — das Vorbild verteilter Gemeinschafts-Backups.',
        actionCardTitle: 'Eine Familiengeschichte oder Sprachaufnahme offline sichern',
        actionCardStep: 'Speichern Sie ein Familienheft, Rezept oder eine Aufnahme eines älteren Menschen auf einem Offline-Stick und geben Sie einer Verwandten eine Kopie.',
        pledgeLabel: 'Ich halte Erinnerung in Gemeinschaftshänden',
        transcript: 'Passende Holztruhen und Speicherkarten leuchten zwischen Nachbarhäusern.'
      },
      realityMeter: {
        reason: 'Scannen und OCR laufen schnell; faire Rechte und Offline-Kopien bleiben dringlich.'
      }
    },
    'andean-water-terraces': {
      originRegion: 'Andenhochland',
      traditionLabel: 'Andenes & Amunas-Gemeinschaften',
      chipTitle: 'Bergwasser über Jahreszeiten hinweg teilen',
      title: 'Andenes & Amunas: Terrassen, die Dörfer nie verdursten lassen',
      summary: 'Präzisionsbewässerung lässt Exporte wachsen — bis Trockenzeit-Quellen oberhalb der Bergstädte versiegen.',
      honestyNote: 'Bodenmodelle helfen heute; Resilienz fußt auf dörflichen Wasserwechseln und Gesteins-Sickerkanälen.',
      dependencyLabel: 'Physische Grundwasser-Speicherdauer bei Ausfall elektrischer Pumpen',
      doorTitle: 'Gemeinwohl',
      reviewer: 'Offen für andine Gemeinschaftsreview',
      wonder: {
        text: 'Entlang sonniger Hänge steuert Toto Nebelfänger und Tropfventile über hunderte Steinterrassen. Ernten reifen gleichmäßig selbst in schneearmen Jahren.',
        totoLine: 'Toto: Jede grüne Stufe hält den Morgentau.',
        transcript: 'Geschwungene grüne Terrassen schmiegen sich an schneebedeckte Andengipfel.'
      },
      wobble: {
        text: 'Wenn Software nur gut vernetzte Tieftäler priorisiert, verfallen obere Steinkanäle (*amunas*) — sodass Hochweiden vertrocknen, sobald Solarsensoren ausfallen.',
        transcript: 'Obere Steinkanäle trocknen aus, während unten Elektropumpen blinken.'
      },
      weight: {
        question: 'Was hält Bergernten stabil — ob das Stromnetz läuft oder ruht?',
        transcript: 'Nachbarn schreiten mit Holzwerkzeug gemeinsam Steinschleusen ab.',
        options: [
          { id: 'a', text: 'Sickerkanäle aus Stein (amunas) pflegen, damit Quellen noch Wochen später fließen.' },
          { id: 'b', text: 'Gemeinsame Wasserrunden (ayni) zwischen oberen und unteren Dörfern schützen.' },
          { id: 'c', text: 'Keine Schleuse ohne einfache hölzerne oder eiserne Handklappe automatisieren.' }
        ]
      },
      way: {
        text: 'Alte *amunas* lehren bis heute Hydrologen: Regenzeit-Bäche in durchlässigen Fels zu leiten speist Quellen noch Monate später ganz ohne Beton oder Cloud-Strom.',
        actionCardTitle: 'Einen passiven Offline-Wasservorrat im Haus halten',
        actionCardStep: 'Halten Sie Trinkwasser für drei Tage und einen einfachen stromlosen Schwerkraftfilter bereit.',
        pledgeLabel: 'Ich halte passive Offline-Resilienz bereit',
        transcript: 'Klares Wasser nährt grüne Terrassen unter klaren Bergkämmen.'
      },
      realityMeter: {
        reason: 'Smarte Bewässerung klappt heute; passive Grundwasserspeisung und Dorfordnung sichern Dürren ab.'
      }
    },
    'japan-craft-repair': {
      originRegion: 'Japan',
      traditionLabel: 'Monozukuri & Kunst des Reparierens',
      chipTitle: 'Jedes Werkzeug herbeirufen, ohne Reparaturwissen zu verlieren',
      title: 'Monozukuri-Tasche: Werkzeuge, die jeder noch öffnen kann',
      summary: 'Jedes Gerät erscheint makellos am Morgen — bis ein Stromausfall Häuser voller verklebter Blackboxes hinterlässt.',
      honestyNote: 'Sofortiges Materialisieren ist Fiktion; verklebte Geräte stellen das Recht auf Reparatur bereits heute auf die Probe.',
      dependencyLabel: 'Stunden funktionierenden Alltags bei Stopp automatisierter Ersatzteil-Logistik',
      doorTitle: 'Alltagstechnik',
      reviewer: 'Offen für japanische Handwerks- und Technikreview',
      wonder: {
        text: 'Gesprungener Reiskocher oder gerissene Fahrradkette — Toto reicht in einem Atemzug ein fabrikneues Ersatzteil ohne Schrottberg.',
        totoLine: 'Toto: Alles Kaputte sauber ausgetauscht.',
        transcript: 'Blankes Werkzeug erscheint auf einer ordentlichen Holzwerkbank.'
      },
      wobble: {
        text: 'Nach Jahren des verklebten Tauschs schließen Eisenwarenhändler und Werkstätten. Als ein Beben Hafenleitungen kappt, fehlt zu Hause jede Schraube und jeder Schaltplan.',
        transcript: 'Glatte schraubenlose Geräte stehen vor einer leeren Werkzeugleiste.'
      },
      weight: {
        question: 'Wenn Maschinen mühelos alles ersetzen — welches Können hält eine Stadt robust?',
        transcript: 'Handwerker richten ein Holzscharnier neben einem Sensormodul aus.',
        options: [
          { id: 'a', text: 'Standard-Schrauben, gedruckte Pläne und echtes Recht auf Reparatur fordern.' },
          { id: 'b', text: 'Nachbarschafts-Werkstätten und Lehrbetriebe trotz Automatisierung fördern.' },
          { id: 'c', text: 'Ersatzteile für freie Techniker öffnen statt für eine einzelne Marke.' }
        ]
      },
      way: {
        text: 'Vom leimfreien Holzverband (*kigumi*) bis zum goldenen Ausbessern (*kintsugi*) ehrt gutes Handwerk das Reparierbare — heute in modularen Geräten und einer kleinen Hauswerkzeugbox.',
        actionCardTitle: 'Handwerkzeug und einen Papierplan griffbereit halten',
        actionCardStep: 'Lernen Sie, Wasserhaupthahn und Hauptsicherung von Hand abzustellen, und legen Sie Basis-Schraubendreher bereit.',
        pledgeLabel: 'Ich pflege handwerkliche Reparatur-Grundlagen',
        transcript: 'Goldene Reparaturfugen glänzen an einem Gefäß neben Werkstattwerkzeugen.'
      },
      realityMeter: {
        reason: 'Taschen-Replikatoren sind Fiktion; verklebte Geräte fordern bereits heute Reparaturrecht heraus.'
      }
    },
    'nordic-right-to-roam': {
      originRegion: 'Nordische Gemeingut-Tradition',
      traditionLabel: 'Allemansrätten & offene Gemeingüter',
      chipTitle: 'Gemeinsame Werkzeuge offenhalten, wenn Arbeit sich automatisiert',
      title: 'Offene Pfade in schneller Zeit: Komfort ohne versteckte Maut',
      summary: 'Digitale Helfer regeln jede Aufgabe — bis öffentliche Wege und Einkommen leise hinter private Schranken wandern.',
      honestyNote: 'Büro-Automatisierung beschleunigt Routine schon heute; offene Standards und soziale Polster entscheiden über Fairness.',
      dependencyLabel: 'Einkommens- und Umschulungspuffer bei Automatisierung von Wissensarbeit',
      doorTitle: 'Alltagstechnik',
      reviewer: 'Offen für nordische Politik- und Bürgerreview',
      wonder: {
        text: 'Kommunen verbinden flinke Assistenten mit öffentlicher Gesundheit, Nahverkehr und freiem Zugang zu Wäldern und Fjorden.',
        totoLine: 'Toto: Jede Erledigung klappt vor dem Frühstück.',
        transcript: 'Ein Holzwegweiser weist zu Kiefern und Fjorden neben einer ruhigen Tramhaltestelle.'
      },
      wobble: {
        text: 'Binnen zweier Winter regeln lizenzierte Plattformen Ämter und Bürojobs — verlangen Gebühren je Anfrage, während Gehälter schneller sinken als Bildungsbudgets wachsen.',
        transcript: 'Drehkreuze stehen quer auf Waldwegen zwischen Wohnviertel und Rathaus.'
      },
      weight: {
        question: 'Wenn Automatisierung Routinen überholt — was lässt jeden Einwohner frei weitergehen?',
        transcript: 'Bürger prüfen offene digitale Standards und lebenslange Bildungsgutscheine.',
        options: [
          { id: 'a', text: 'Produktivitätsgewinne an tragfähige Einkommenspuffer und Weiterbildung koppeln.' },
          { id: 'b', text: 'Öffentliche Digitaldienste auf offenen Standards ohne Monopolbindung halten.' },
          { id: 'c', text: 'Bildschirmfreie öffentliche Räume und persönliche Sachbearbeitung gesetzlich schützen.' }
        ]
      },
      way: {
        text: 'Das nordische *Allemansrätten* garantiert freien Durchgang bei Achtsamkeit gegenüber der Natur — ein klarer Kompass für offene öffentliche KI-Standards und sozialen Schutz.',
        actionCardTitle: 'Prüfen, ob örtliche Dienste eine offene Tür behalten',
        actionCardStep: 'Vergewissern Sie sich, dass Amt, Bank oder Praxis neben Apps noch Telefon- oder Vor-Ort-Schalter führen.',
        pledgeLabel: 'Ich schütze offenen bürgernahen Zugang',
        transcript: 'Offene Kiefernpfade liegen neben Holzbänken vor ruhigen Fjorden.'
      },
      realityMeter: {
        reason: 'Wissens-Automatisierung findet heute statt; offene Normen und soziale Puffer stabilisieren.'
      }
    },
    'anatolia-mediterranean-crossroads': {
      originRegion: 'Östliches Mittelmeer & Anatolien',
      traditionLabel: 'Steinkreuzungen & Bürgerplätze',
      chipTitle: 'Gemeinsame Plätze auch in Krisen ruhig halten',
      title: 'Kreuzungen aus Stein: digitale Zwillinge, die Erde und Nachbarn achten',
      summary: 'Smarte Stadttafeln lenken Fähren und Plätze — bis Erdstöße Funkmasten rund um Altstadtplätze abschalten.',
      honestyNote: 'Digitale Stadtzwillinge laufen heute; reale Erdbebensicherheit und Offline-Sammelpunkte geben den Ausschlag.',
      dependencyLabel: 'Stromnetz-Ausdauer und Quartier-Sammelbereitschaft in historischen Hafenstädten',
      doorTitle: 'Kultur & Kreativität',
      reviewer: 'Offen für türkische, griechische und mediterrane Review',
      wonder: {
        text: 'Vom Bosporus bis zur Ägäis stimmt Toto Morgenfähren, Mauerwerkssensoren und Schattendächer ab, damit alte Viertel kühl und einladend bleiben.',
        totoLine: 'Toto: Fähren, Bahnen und Plätze fließen als Eins.',
        transcript: 'Weiße Fähren gleiten an Steinbögen und Zypressen vorüber.'
      },
      wobble: {
        text: 'Das blinde Vertrauen auf Cloud-Sensoren strich Aushänge und echte Räumungsübungen — sodass Familien bei Mobilfunkausfall nicht wissen, welcher Platz sicher ist.',
        transcript: 'Stumme Handys blinken neben dunklen Anzeigen und trockenem Steinbrunnen.'
      },
      weight: {
        question: 'Wenn Stadtnetze bei Sturm oder Beben ausfallen — was sammelt Nachbarn am schnellsten?',
        transcript: 'Nachbarn kommen um eine schattige Zisterne und eine Kreidetafel zusammen.',
        options: [
          { id: 'a', text: 'Stromlose offene Sammelplätze, Wasserstellen und Papierkarten in jedem Viertel halten.' },
          { id: 'b', text: 'Erst in stabile Gebäudeverstärkung investieren, bevor schicke Dashboards folgen.' },
          { id: 'c', text: 'Ladeninhaber und Blockpaten als direkte Nachbarschaftshelfer schulen.' }
        ]
      },
      way: {
        text: 'Über Jahrhunderte überstanden Viertel am Mittelmeer Erschütterungen durch offene Plätze, Schwerkraft-Zisternen und dichte Nachbarschaftshilfe — Architektur, die kein Softwarefehler abschaltet.',
        actionCardTitle: 'Den offenen Sammelplatz des eigenen Viertels kennen',
        actionCardStep: 'Vereinbaren Sie im Haushalt einen freien Park oder Platz in zehn Minuten Gehweite für den Fall toter Netze.',
        pledgeLabel: 'Ich kenne unseren Offline-Treffpunkt',
        transcript: 'Olivenbäume rahmen einen sonnigen Steinplatz mit Wasserhähnen und klaren Schildern.'
      },
      realityMeter: {
        reason: 'Urbane digitale Steuerung existiert heute; physische Bausicherheit und Offline-Treffpunkte stehen voran.'
      }
    }
  }
};

import json

cards_text = '''
001 ■ Tangela
002 ■ Tangrowth
003 ■ Pinsir
004 ■ Spinarak
005 ■ Ariados
006 ■ Sunkern
007 ■ Sunflora
008 ■ Heracross
009 ■ Volbeat
010 ■ Illumise
011 ■ Leafeon
012 ■ Phantump
013 ■ Trevenant
014 ■ Grookey
015 ■ Thwackey
016 ■ Rillaboom
017 ■ Applin
018 ■ Dipplin
019 ■ Iron Leaves
020 ■ Poltchageist
021 ■ Poltchageist
022 ■ Sinistcha
023 ■ Sinistcha ex
024 ■ Teal Mask Ogerpon
025 ■ Teal Mask Ogerpon ex
026 ■ Vulpix
027 ■ Ninetales
028 ■ Slugma
029 ■ Magcargo ex
030 ■ Torkoal
031 ■ Chimchar
032 ■ Monferno
033 ■ Infernape
034 ■ Darumaka
035 ■ Darmanitan
036 ■ Litwick
037 ■ Lampent
038 ■ Chandelure
039 ■ Chi-Yu
040 ■ Hearthflame Mask Ogerpon ex
041 ■ Poliwag
042 ■ Poliwhirl
043 ■ Poliwrath
044 ■ Goldeen
045 ■ Seaking
046 ■ Jynx
047 ■ Corphish
048 ■ Crawdaunt
049 ■ Feebas
050 ■ Milotic
051 ■ Snorunt
052 ■ Glalie
053 ■ Froslass
054 ■ Glaceon
055 ■ Phione
056 ■ Froakie
057 ■ Frogadier
058 ■ Cramorant
059 ■ Finizen
060 ■ Palafin
061 ■ Palafin ex
062 ■ Iron Bundle
063 ■ Walking Wake
064 ■ Wellspring Mask Ogerpon ex
065 ■ Zapdos
066 ■ Shinx
067 ■ Luxio
068 ■ Luxray ex
069 ■ Emolga
070 ■ Helioptile
071 ■ Heliolisk
072 ■ Morpeko
073 ■ Tadbulb
074 ■ Bellibolt
075 ■ Wattrel
076 ■ Kilowattrel
077 ■ Iron Thorns ex
078 ■ Clefairy
079 ■ Clefable
080 ■ Abra
081 ■ Kadabra
082 ■ Alakazam
083 ■ Girafarig
084 ■ Farigiraf
085 ■ Chimecho
086 ■ Flabébé
087 ■ Floette
088 ■ Florges
089 ■ Swirlix
090 ■ Slurpuff
091 ■ Sandygast
092 ■ Palossand
093 ■ Enamorus
094 ■ Scream Tail ex
095 ■ Munkidori
096 ■ Fezandipiti
097 ■ Sandshrew
098 ■ Sandslash
099 ■ Hisuian Growlithe
100 ■ Hisuian Arcanine
101 ■ Nosepass
102 ■ Probopass
103 ■ Timburr
104 ■ Gurdurr
105 ■ Conkeldurr
106 ■ Greninja ex
107 ■ Hawlucha
108 ■ Glimmet
109 ■ Glimmora
110 ■ Ting-Lu
111 ■ Okidogi
112 ■ Cornerstone Mask Ogerpon ex
113 ■ Poochyena
114 ■ Mightyena
115 ■ Venipede
116 ■ Whirlipede
117 ■ Scolipede
118 ■ Brute Bonnet
119 ■ Skarmory
120 ■ Aron
121 ■ Lairon
122 ■ Aggron
123 ■ Heatran
124 ■ Varoom
125 ■ Revavroom
126 ■ Applin
127 ■ Dipplin
128 ■ Dreepy
129 ■ Drakloak
130 ■ Dragapult ex
131 ■ Tatsugiri
132 ■ Farfetch’d
133 ■ Chansey
134 ■ Blissey ex
135 ■ Eevee
136 ■ Snorlax
137 ■ Aipom
138 ■ Ambipom
139 ■ Ducklett
140 ■ Swanna
141 ■ Bloodmoon Ursaluna ex
142 ■ Accompanying Flute
143 ■ Bug Catching Set
144 ■ Caretaker
145 ■ Carmine
146 ■ Community Center
147 ■ Cook
148 ■ Enhanced Hammer
149 ■ Festival Grounds
150 ■ Handheld Circulator
151 ■ Hassel
152 ■ Hyper Aroma
153 ■ Jamming Tower
154 ■ Kieran
155 ■ Lana’s Aid
156 ■ Love Ball
157 ■ Lucian
158 ■ Lucky Helmet
159 ■ Ogre’s Mask
160 ■ Perrin
161 ■ Raifort
162 ■ Scoop Up Cyclone
163 ■ Secret Box
164 ■ Survival Brace
165 ■ Unfair Stamp
166 ■ Boomerang Energy
167 ■ Legacy Energy
168 ■ Pinsir
169 ■ Sunflora
170 ■ Dipplin
171 ■ Poltchageist
172 ■ Torkoal
173 ■ Infernape
174 ■ Froslass
175 ■ Phione
176 ■ Cramorant
177 ■ Heliolisk
178 ■ Wattrel
179 ■ Chimecho
180 ■ Enamorus
181 ■ Hisuian Growlithe
182 ■ Probopass
183 ■ Timburr
184 ■ Lairon
185 ■ Applin
186 ■ Tatsugiri
187 ■ Chansey
188 ■ Eevee
189 ■ Sinistcha ex
190 ■ Teal Mask Ogerpon ex
191 ■ Magcargo ex
192 ■ Hearthflame Mask Ogerpon ex
193 ■ Palafin ex
194 ■ Wellspring Mask Ogerpon ex
195 ■ Luxray ex
196 ■ Iron Thorns ex
197 ■ Scream Tail ex
198 ■ Greninja ex
199 ■ Cornerstone Mask Ogerpon ex
200 ■ Dragapult ex
201 ■ Blissey ex
202 ■ Bloodmoon Ursaluna ex
203 ■ Caretaker
204 ■ Carmine
205 ■ Hassel
206 ■ Kieran
207 ■ Lana’s Aid
208 ■ Lucian
209 ■ Perrin
210 ■ Sinistcha ex
211 ■ Teal Mask Ogerpon ex
212 ■ Hearthflame Mask Ogerpon ex
213 ■ Wellspring Mask Ogerpon ex
214 ■ Greninja ex
215 ■ Cornerstone Mask Ogerpon ex
216 ■ Bloodmoon Ursaluna ex
217 ■ Carmine
218 ■ Kieran
219 ■ Lana’s Aid
220 ■ Perrin
221 ■ Teal Mask Ogerpon ex
222 ■ Bloodmoon Ursaluna ex
223 ■ Buddy-Buddy Poffin
224 ■ Enhanced Hammer
225 ■ Rescue Board
226 ■ Luminous Energy
'''

cards = []
for line in cards_text.strip().split('\n'):
    if line.strip():
        parts = line.strip().split('■')
        identifier = parts[0].strip().zfill(3)
        name = parts[1].strip()
        card = {
            "identifier": identifier,
            "name": name,
            "rarity": "Common"
        }
        cards.append(card)

data = {
    "collection_name": "Twilight Masquerade",
    "cards": cards
}

with open('twilight_masquerade.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
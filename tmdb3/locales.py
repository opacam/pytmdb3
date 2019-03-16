#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------
# Name: locales.py    Stores locale information for filtering results
# Python Library
# Author: Raymond Wagner
# -----------------------

from .tmdb_exceptions import *
import locale

syslocale = None


class LocaleBase(object):
    __slots__ = ['__immutable']
    _stored = {}
    fallthrough = False

    def __init__(self, *keys):
        for key in keys:
            self._stored[key.lower()] = self
        self.__immutable = True

    def __setattr__(self, key, value):
        if getattr(self, '__immutable', False):
            raise NotImplementedError(self.__class__.__name__ +
                                      ' does not support modification.')
        super(LocaleBase, self).__setattr__(key, value)

    def __delattr__(self, key):
        if getattr(self, '__immutable', False):
            raise NotImplementedError(self.__class__.__name__ +
                                      ' does not support modification.')
        super(LocaleBase, self).__delattr__(key)

    def __lt__(self, other):
        return (id(self) != id(other)) and (str(self) > str(other))

    def __gt__(self, other):
        return (id(self) != id(other)) and (str(self) < str(other))

    def __eq__(self, other):
        return (id(self) == id(other)) or (str(self) == str(other))

    @classmethod
    def getstored(cls, key):
        if key is None:
            return None
        try:
            return cls._stored[key.lower()]
        except:
            raise TMDBLocaleError(
                f"'{key}' is not a known valid {cls.__name__} code.")


class Language(LocaleBase):
    __slots__ = ['ISO639_1', 'ISO639_2', 'ISO639_2B', 'englishname',
                 'nativename']
    _stored = {}

    def __init__(self, iso1, iso2, ename):
        self.ISO639_1 = iso1
        self.ISO639_2 = iso2
        # self.ISO639_2B = iso2b
        self.englishname = ename
        # self.nativename = nname
        super(Language, self).__init__(iso1, iso2)

    def __str__(self):
        return self.ISO639_1

    def __repr__(self):
        return f"<Language '{self.englishname}' ({self.ISO639_1})>"


class Country(LocaleBase):
    __slots__ = ['alpha2', 'name']
    _stored = {}

    def __init__(self, alpha2, name):
        self.alpha2 = alpha2
        self.name = name
        super(Country, self).__init__(alpha2)

    def __str__(self):
        return self.alpha2

    def __repr__(self):
        return f"<Country '{self.name}' ({self.alpha2})>"


class Locale(LocaleBase):
    __slots__ = ['language', 'country', 'encoding']

    def __init__(self, language, country, encoding, *keys):
        self.language = Language.getstored(language)
        self.country = Country.getstored(country)
        self.encoding = encoding if encoding else 'latin-1'
        super(Locale, self).__init__(*keys)

    def __str__(self):
        return f"{self.language}_{self.country}"

    def __repr__(self):
        return f"<Locale {self.language}_{self.country}>"

    def encode(self, dat):
        """Encode using system default encoding for network/file output."""
        try:
            return dat.encode(self.encoding)
        except AttributeError:
            # not a string type, pass along
            return dat
        except UnicodeDecodeError:
            # just return unmodified and hope for the best
            return dat

    def decode(self, dat):
        """Decode to system default encoding for internal use."""
        try:
            return dat.decode(self.encoding)
        except AttributeError:
            # not a string type, pass along
            return dat
        except UnicodeEncodeError:
            # just return unmodified and hope for the best
            return dat


def set_locale(language=None, country=None, fallthrough=False):
    global syslocale
    LocaleBase.fallthrough = fallthrough

    sysloc, sysenc = locale.getdefaultlocale()

    if (not language) or (not country):
        dat = None
        if syslocale is not None:
            dat = (str(syslocale.language), str(syslocale.country))
        else:
            if (sysloc is None) or ('_' not in sysloc):
                dat = ('en', 'US')
            else:
                dat = sysloc.split('_')
        if language is None:
            language = dat[0]
        if country is None:
            country = dat[1]

    syslocale = Locale(language, country, sysenc)


def get_locale(language=-1, country=-1):
    """Output locale using provided attributes, or return system locale."""
    global syslocale
    # pull existing stored values
    if syslocale is None:
        loc = Locale(None, None, locale.getdefaultlocale()[1])
    else:
        loc = syslocale

    # both options are default, return stored values
    if language == country == -1:
        return loc

    # supplement default option with stored values
    if language == -1:
        language = loc.language
    elif country == -1:
        country = loc.country
    return Locale(language, country, loc.encoding)


# ******** AUTOGENERATED LANGUAGE AND COUNTRY DATA BELOW HERE ********

Language("ab", "abk", "Abkhazian")
Language("aa", "aar", "Afar")
Language("af", "afr", "Afrikaans")
Language("ak", "aka", "Akan")
Language("sq", "alb/sqi", "Albanian")
Language("am", "amh", "Amharic")
Language("ar", "ara", "Arabic")
Language("an", "arg", "Aragonese")
Language("hy", "arm/hye", "Armenian")
Language("as", "asm", "Assamese")
Language("av", "ava", "Avaric")
Language("ae", "ave", "Avestan")
Language("ay", "aym", "Aymara")
Language("az", "aze", "Azerbaijani")
Language("bm", "bam", "Bambara")
Language("ba", "bak", "Bashkir")
Language("eu", "baq/eus", "Basque")
Language("be", "bel", "Belarusian")
Language("bn", "ben", "Bengali")
Language("bh", "bih", "Bihari languages")
Language("bi", "bis", "Bislama")
Language("nb", "nob", "Bokmål, Norwegian")
Language("bs", "bos", "Bosnian")
Language("br", "bre", "Breton")
Language("bg", "bul", "Bulgarian")
Language("my", "bur/mya", "Burmese")
Language("es", "spa", "Castilian")
Language("ca", "cat", "Catalan")
Language("km", "khm", "Central Khmer")
Language("ch", "cha", "Chamorro")
Language("ce", "che", "Chechen")
Language("ny", "nya", "Chewa")
Language("ny", "nya", "Chichewa")
Language("zh", "chi/zho", "Chinese")
Language("za", "zha", "Chuang")
Language("cu", "chu", "Church Slavic")
Language("cu", "chu", "Church Slavonic")
Language("cv", "chv", "Chuvash")
Language("kw", "cor", "Cornish")
Language("co", "cos", "Corsican")
Language("cr", "cre", "Cree")
Language("hr", "hrv", "Croatian")
Language("cs", "cze/ces", "Czech")
Language("da", "dan", "Danish")
Language("dv", "div", "Dhivehi")
Language("dv", "div", "Divehi")
Language("nl", "dut/nld", "Dutch")
Language("dz", "dzo", "Dzongkha")
Language("en", "eng", "English")
Language("eo", "epo", "Esperanto")
Language("et", "est", "Estonian")
Language("ee", "ewe", "Ewe")
Language("fo", "fao", "Faroese")
Language("fj", "fij", "Fijian")
Language("fi", "fin", "Finnish")
Language("nl", "dut/nld", "Flemish")
Language("fr", "fre/fra", "French")
Language("ff", "ful", "Fulah")
Language("gd", "gla", "Gaelic")
Language("gl", "glg", "Galician")
Language("lg", "lug", "Ganda")
Language("ka", "geo/kat", "Georgian")
Language("de", "ger/deu", "German")
Language("ki", "kik", "Gikuyu")
Language("el", "gre/ell", "Greek, Modern (1453-)")
Language("kl", "kal", "Greenlandic")
Language("gn", "grn", "Guarani")
Language("gu", "guj", "Gujarati")
Language("ht", "hat", "Haitian")
Language("ht", "hat", "Haitian Creole")
Language("ha", "hau", "Hausa")
Language("he", "heb", "Hebrew")
Language("hz", "her", "Herero")
Language("hi", "hin", "Hindi")
Language("ho", "hmo", "Hiri Motu")
Language("hu", "hun", "Hungarian")
Language("is", "ice/isl", "Icelandic")
Language("io", "ido", "Ido")
Language("ig", "ibo", "Igbo")
Language("id", "ind", "Indonesian")
Language("ia", "ina", "Interlingua (International Auxiliary Language Association)")
Language("ie", "ile", "Interlingue")
Language("iu", "iku", "Inuktitut")
Language("ik", "ipk", "Inupiaq")
Language("ga", "gle", "Irish")
Language("it", "ita", "Italian")
Language("ja", "jpn", "Japanese")
Language("jv", "jav", "Javanese")
Language("kl", "kal", "Kalaallisut")
Language("kn", "kan", "Kannada")
Language("kr", "kau", "Kanuri")
Language("ks", "kas", "Kashmiri")
Language("kk", "kaz", "Kazakh")
Language("ki", "kik", "Kikuyu")
Language("rw", "kin", "Kinyarwanda")
Language("ky", "kir", "Kirghiz")
Language("kv", "kom", "Komi")
Language("kg", "kon", "Kongo")
Language("ko", "kor", "Korean")
Language("kj", "kua", "Kuanyama")
Language("ku", "kur", "Kurdish")
Language("kj", "kua", "Kwanyama")
Language("ky", "kir", "Kyrgyz")
Language("lo", "lao", "Lao")
Language("la", "lat", "Latin")
Language("lv", "lav", "Latvian")
Language("lb", "ltz", "Letzeburgesch")
Language("li", "lim", "Limburgan")
Language("li", "lim", "Limburger")
Language("li", "lim", "Limburgish")
Language("ln", "lin", "Lingala")
Language("lt", "lit", "Lithuanian")
Language("lu", "lub", "Luba-Katanga")
Language("lb", "ltz", "Luxembourgish")
Language("mk", "mac/mkd", "Macedonian")
Language("mg", "mlg", "Malagasy")
Language("ms", "may/msa", "Malay")
Language("ml", "mal", "Malayalam")
Language("dv", "div", "Maldivian")
Language("mt", "mlt", "Maltese")
Language("gv", "glv", "Manx")
Language("mi", "mao/mri", "Maori")
Language("mr", "mar", "Marathi")
Language("mh", "mah", "Marshallese")
Language("ro", "rum/ron", "Moldavian")
Language("ro", "rum/ron", "Moldovan")
Language("mn", "mon", "Mongolian")
Language("na", "nau", "Nauru")
Language("nv", "nav", "Navaho")
Language("nv", "nav", "Navajo")
Language("nd", "nde", "Ndebele, North")
Language("nr", "nbl", "Ndebele, South")
Language("ng", "ndo", "Ndonga")
Language("ne", "nep", "Nepali")
Language("nd", "nde", "North Ndebele")
Language("se", "sme", "Northern Sami")
Language("no", "nor", "Norwegian")
Language("nb", "nob", "Norwegian Bokmål")
Language("nn", "nno", "Norwegian Nynorsk")
Language("ii", "iii", "Nuosu")
Language("ny", "nya", "Nyanja")
Language("nn", "nno", "Nynorsk, Norwegian")
Language("ie", "ile", "Occidental")
Language("oc", "oci", "Occitan (post 1500)")
Language("oj", "oji", "Ojibwa")
Language("cu", "chu", "Old Bulgarian")
Language("cu", "chu", "Old Church Slavonic")
Language("cu", "chu", "Old Slavonic")
Language("or", "ori", "Oriya")
Language("om", "orm", "Oromo")
Language("os", "oss", "Ossetian")
Language("os", "oss", "Ossetic")
Language("pi", "pli", "Pali")
Language("pa", "pan", "Panjabi")
Language("ps", "pus", "Pashto")
Language("fa", "per/fas", "Persian")
Language("pl", "pol", "Polish")
Language("pt", "por", "Portuguese")
Language("pa", "pan", "Punjabi")
Language("ps", "pus", "Pushto")
Language("qu", "que", "Quechua")
Language("ro", "rum/ron", "Romanian")
Language("rm", "roh", "Romansh")
Language("rn", "run", "Rundi")
Language("ru", "rus", "Russian")
Language("sm", "smo", "Samoan")
Language("sg", "sag", "Sango")
Language("sa", "san", "Sanskrit")
Language("sc", "srd", "Sardinian")
Language("gd", "gla", "Scottish Gaelic")
Language("sr", "srp", "Serbian")
Language("sn", "sna", "Shona")
Language("ii", "iii", "Sichuan Yi")
Language("sd", "snd", "Sindhi")
Language("si", "sin", "Sinhala")
Language("si", "sin", "Sinhalese")
Language("sk", "slo/slk", "Slovak")
Language("sl", "slv", "Slovenian")
Language("so", "som", "Somali")
Language("st", "sot", "Sotho, Southern")
Language("nr", "nbl", "South Ndebele")
Language("es", "spa", "Spanish")
Language("su", "sun", "Sundanese")
Language("sw", "swa", "Swahili")
Language("ss", "ssw", "Swati")
Language("sv", "swe", "Swedish")
Language("tl", "tgl", "Tagalog")
Language("ty", "tah", "Tahitian")
Language("tg", "tgk", "Tajik")
Language("ta", "tam", "Tamil")
Language("tt", "tat", "Tatar")
Language("te", "tel", "Telugu")
Language("th", "tha", "Thai")
Language("bo", "tib/bod", "Tibetan")
Language("ti", "tir", "Tigrinya")
Language("to", "ton", "Tonga (Tonga Islands)")
Language("ts", "tso", "Tsonga")
Language("tn", "tsn", "Tswana")
Language("tr", "tur", "Turkish")
Language("tk", "tuk", "Turkmen")
Language("tw", "twi", "Twi")
Language("ug", "uig", "Uighur")
Language("uk", "ukr", "Ukrainian")
Language("ur", "urd", "Urdu")
Language("ug", "uig", "Uyghur")
Language("uz", "uzb", "Uzbek")
Language("ca", "cat", "Valencian")
Language("ve", "ven", "Venda")
Language("vi", "vie", "Vietnamese")
Language("vo", "vol", "Volapük")
Language("wa", "wln", "Walloon")
Language("cy", "wel/cym", "Welsh")
Language("fy", "fry", "Western Frisian")
Language("wo", "wol", "Wolof")
Language("xh", "xho", "Xhosa")
Language("yi", "yid", "Yiddish")
Language("yo", "yor", "Yoruba")
Language("za", "zha", "Zhuang")
Language("zu", "zul", "Zulu")
Country("AD", "Andorra")
Country("AE", "United Arab Emirates")
Country("AF", "Afghanistan")
Country("AG", "Antigua and Barbuda")
Country("AI", "Anguilla")
Country("AL", "Albania")
Country("AM", "Armenia")
Country("AO", "Angola")
Country("AQ", "Antarctica")
Country("AR", "Argentina")
Country("AS", "American Samoa")
Country("AT", "Austria")
Country("AU", "Australia")
Country("AW", "Aruba")
Country("AX", "Åland Islands")
Country("AZ", "Azerbaijan")
Country("BA", "Bosnia and Herzegovina")
Country("BB", "Barbados")
Country("BD", "Bangladesh")
Country("BE", "Belgium")
Country("BF", "Burkina Faso")
Country("BG", "Bulgaria")
Country("BH", "Bahrain")
Country("BI", "Burundi")
Country("BJ", "Benin")
Country("BL", "Saint Barthélemy")
Country("BM", "Bermuda")
Country("BN", "Brunei Darussalam")
Country("BO", "Bolivia (Plurinational State of)")
Country("BQ", "Bonaire, Sint Eustatius and Saba")
Country("BR", "Brazil")
Country("BS", "Bahamas")
Country("BT", "Bhutan")
Country("BV", "Bouvet Island")
Country("BW", "Botswana")
Country("BY", "Belarus")
Country("BZ", "Belize")
Country("CA", "Canada")
Country("CC", "Cocos (Keeling) Islands")
Country("CD", "Congo, Democratic Republic of the")
Country("CF", "Central African Republic")
Country("CG", "Congo")
Country("CH", "Switzerland")
Country("CI", "Côte d'Ivoire")
Country("CK", "Cook Islands")
Country("CL", "Chile")
Country("CM", "Cameroon")
Country("CN", "China")
Country("CO", "Colombia")
Country("CR", "Costa Rica")
Country("CU", "Cuba")
Country("CV", "Cabo Verde")
Country("CW", "Curaçao")
Country("CX", "Christmas Island")
Country("CY", "Cyprus")
Country("CZ", "Czechia")
Country("DE", "Germany")
Country("DJ", "Djibouti")
Country("DK", "Denmark")
Country("DM", "Dominica")
Country("DO", "Dominican Republic")
Country("DZ", "Algeria")
Country("EC", "Ecuador")
Country("EE", "Estonia")
Country("EG", "Egypt")
Country("EH", "Western Sahara")
Country("ER", "Eritrea")
Country("ES", "Spain")
Country("ET", "Ethiopia")
Country("FI", "Finland")
Country("FJ", "Fiji")
Country("FK", "Falkland Islands (Malvinas)")
Country("FM", "Micronesia (Federated States of)")
Country("FO", "Faroe Islands")
Country("FR", "France")
Country("GA", "Gabon")
Country("GB", "United Kingdom of Great Britain and Northern Ireland")
Country("GD", "Grenada")
Country("GE", "Georgia")
Country("GF", "French Guiana")
Country("GG", "Guernsey")
Country("GH", "Ghana")
Country("GI", "Gibraltar")
Country("GL", "Greenland")
Country("GM", "Gambia")
Country("GN", "Guinea")
Country("GP", "Guadeloupe")
Country("GQ", "Equatorial Guinea")
Country("GR", "Greece")
Country("GS", "South Georgia and the South Sandwich Islands")
Country("GT", "Guatemala")
Country("GU", "Guam")
Country("GW", "Guinea-Bissau")
Country("GY", "Guyana")
Country("HK", "Hong Kong")
Country("HM", "Heard Island and McDonald Islands")
Country("HN", "Honduras")
Country("HR", "Croatia")
Country("HT", "Haiti")
Country("HU", "Hungary")
Country("ID", "Indonesia")
Country("IE", "Ireland")
Country("IL", "Israel")
Country("IM", "Isle of Man")
Country("IN", "India")
Country("IO", "British Indian Ocean Territory")
Country("IQ", "Iraq")
Country("IR", "Iran (Islamic Republic of)")
Country("IS", "Iceland")
Country("IT", "Italy")
Country("JE", "Jersey")
Country("JM", "Jamaica")
Country("JO", "Jordan")
Country("JP", "Japan")
Country("KE", "Kenya")
Country("KG", "Kyrgyzstan")
Country("KH", "Cambodia")
Country("KI", "Kiribati")
Country("KM", "Comoros")
Country("KN", "Saint Kitts and Nevis")
Country("KP", "Korea (Democratic People's Republic of)")
Country("KR", "Korea, Republic of")
Country("KW", "Kuwait")
Country("KY", "Cayman Islands")
Country("KZ", "Kazakhstan")
Country("LA", "Lao People's Democratic Republic")
Country("LB", "Lebanon")
Country("LC", "Saint Lucia")
Country("LI", "Liechtenstein")
Country("LK", "Sri Lanka")
Country("LR", "Liberia")
Country("LS", "Lesotho")
Country("LT", "Lithuania")
Country("LU", "Luxembourg")
Country("LV", "Latvia")
Country("LY", "Libya")
Country("MA", "Morocco")
Country("MC", "Monaco")
Country("MD", "Moldova, Republic of")
Country("ME", "Montenegro")
Country("MF", "Saint Martin (French part)")
Country("MG", "Madagascar")
Country("MH", "Marshall Islands")
Country("MK", "North Macedonia")
Country("ML", "Mali")
Country("MM", "Myanmar")
Country("MN", "Mongolia")
Country("MO", "Macao")
Country("MP", "Northern Mariana Islands")
Country("MQ", "Martinique")
Country("MR", "Mauritania")
Country("MS", "Montserrat")
Country("MT", "Malta")
Country("MU", "Mauritius")
Country("MV", "Maldives")
Country("MW", "Malawi")
Country("MX", "Mexico")
Country("MY", "Malaysia")
Country("MZ", "Mozambique")
Country("NA", "Namibia")
Country("NC", "New Caledonia")
Country("NE", "Niger")
Country("NF", "Norfolk Island")
Country("NG", "Nigeria")
Country("NI", "Nicaragua")
Country("NL", "Netherlands[note 1]")
Country("NO", "Norway")
Country("NP", "Nepal")
Country("NR", "Nauru")
Country("NU", "Niue")
Country("NZ", "New Zealand")
Country("OM", "Oman")
Country("PA", "Panama")
Country("PE", "Peru")
Country("PF", "French Polynesia")
Country("PG", "Papua New Guinea")
Country("PH", "Philippines")
Country("PK", "Pakistan")
Country("PL", "Poland")
Country("PM", "Saint Pierre and Miquelon")
Country("PN", "Pitcairn")
Country("PR", "Puerto Rico")
Country("PS", "Palestine, State of")
Country("PT", "Portugal")
Country("PW", "Palau")
Country("PY", "Paraguay")
Country("QA", "Qatar")
Country("RE", "Réunion")
Country("RO", "Romania")
Country("RS", "Serbia")
Country("RU", "Russian Federation")
Country("RW", "Rwanda")
Country("SA", "Saudi Arabia")
Country("SB", "Solomon Islands")
Country("SC", "Seychelles")
Country("SD", "Sudan")
Country("SE", "Sweden")
Country("SG", "Singapore")
Country("SH", "Saint Helena, Ascension and Tristan da Cunha")
Country("SI", "Slovenia")
Country("SJ", "Svalbard and Jan Mayen")
Country("SK", "Slovakia")
Country("SL", "Sierra Leone")
Country("SM", "San Marino")
Country("SN", "Senegal")
Country("SO", "Somalia")
Country("SR", "Suriname")
Country("SS", "South Sudan")
Country("ST", "Sao Tome and Principe")
Country("SV", "El Salvador")
Country("SX", "Sint Maarten (Dutch part)")
Country("SY", "Syrian Arab Republic")
Country("SZ", "Eswatini")
Country("TC", "Turks and Caicos Islands")
Country("TD", "Chad")
Country("TF", "French Southern Territories")
Country("TG", "Togo")
Country("TH", "Thailand")
Country("TJ", "Tajikistan")
Country("TK", "Tokelau")
Country("TL", "Timor-Leste")
Country("TM", "Turkmenistan")
Country("TN", "Tunisia")
Country("TO", "Tonga")
Country("TR", "Turkey")
Country("TT", "Trinidad and Tobago")
Country("TV", "Tuvalu")
Country("TW", "Taiwan, Province of China [note 2]")
Country("TZ", "Tanzania, United Republic of")
Country("UA", "Ukraine")
Country("UG", "Uganda")
Country("UM", "United States Minor Outlying Islands")
Country("US", "United States of America")
Country("UY", "Uruguay")
Country("UZ", "Uzbekistan")
Country("VA", "Holy See")
Country("VC", "Saint Vincent and the Grenadines")
Country("VE", "Venezuela (Bolivarian Republic of)")
Country("VG", "Virgin Islands (British)")
Country("VI", "Virgin Islands (U.S.)")
Country("VN", "Viet Nam")
Country("VU", "Vanuatu")
Country("WF", "Wallis and Futuna")
Country("WS", "Samoa")
Country("YE", "Yemen")
Country("YT", "Mayotte")
Country("ZA", "South Africa")
Country("ZM", "Zambia")
Country("ZW", "Zimbabwe")

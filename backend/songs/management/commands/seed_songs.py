"""
Management command: seed_songs
Loads the parish song catalogue and creates the default admin users.
Run with: python manage.py seed_songs
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from songs.models import Song

User = get_user_model()

# ---------------------------------------------------------------------------
# Song data — all songs used by the parish choir
# ---------------------------------------------------------------------------
SONGS = [
    # ── ENTRANCE ──────────────────────────────────────────────────────────
    {
        'title': 'Nalifurahi Waliponiambia',
        'category': 'Entrance',
        'language': 'Swahili',
        'key_signature': 'G',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Nalifurahi waliponiambia,\n"
            "Twende nyumbani mwa Bwana.\n"
            "Miguu yetu itasimama,\n"
            "Katika malango yako, ee Yerusalemu.\n\n"
            "Kama mji uliounganishwa pamoja,\n"
            "Ndivyo Yerusalemu ilivyo.\n"
            "Makabila yote ya Bwana,\n"
            "Yanakwenda huko kumsifu Bwana.\n\n"
            "Naombeeni amani Yerusalemu,\n"
            "Wapendao wakuwe na raha.\n"
            "Amani iwe ndani yako,\n"
            "Starehe katika minara yako."
        ),
    },
    {
        'title': 'Twende Nyumbani mwa Bwana',
        'category': 'Entrance',
        'language': 'Swahili',
        'key_signature': 'D',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Twende nyumbani mwa Bwana,\n"
            "Furaha na shangwe moyoni,\n"
            "Tumekuja kumwabudu Mungu,\n"
            "Kwa moyo wote wa kweli.\n\n"
            "Nakufurahi, ee Bwana,\n"
            "Katika hekalu lako takatifu,\n"
            "Mikono juu, mioyo juu,\n"
            "Tunamsifu Mungu wetu.\n\n"
            "Twende, twende pamoja,\n"
            "Katika nyumba ya Mungu wetu,\n"
            "Tutoe sifa na shukrani,\n"
            "Kwa Mungu wa milele."
        ),
    },
    {
        'title': 'Hodi Nimeingia',
        'category': 'Entrance',
        'language': 'Swahili',
        'key_signature': 'F',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Hodi nimeingia,\n"
            "Katika nyumba yako Bwana,\n"
            "Hodi nimeingia,\n"
            "Kwa furaha na shukrani.\n\n"
            "Nakuja mbele yako,\n"
            "Na mikono wazi,\n"
            "Nakuja kukuabudu,\n"
            "Ee Mungu wa milele.\n\n"
            "Ninaposimama hapa,\n"
            "Mbele ya kiti chako,\n"
            "Nipokee, ee Bwana,\n"
            "Kwa huruma yako yote."
        ),
    },
    {
        'title': 'Uninyunyuzie Maji',
        'category': 'Entrance',
        'language': 'Swahili',
        'key_signature': 'C',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Uninyunyuzie maji, ee Bwana,\n"
            "Nitakuwa safi na weupe kama theluji.\n"
            "Unioshe, Bwana, nitakuwa safi,\n"
            "Unioshee, nitakuwa mweupe.\n\n"
            "Nami nitaimba sifa zako,\n"
            "Ee Bwana Mungu wangu.\n"
            "Uninyunyuzie maji,\n"
            "Nitakuwa safi na weupe.\n\n"
            "Ondoa madhambi yangu yote,\n"
            "Usafi wako uniingie,\n"
            "Unioshee kwa huruma yako,\n"
            "Nifunikwe na neema yako."
        ),
    },

    # ── BIBLE PROCESSION ──────────────────────────────────────────────────
    {
        'title': 'Nimesikia Bwana Waniita',
        'category': 'Bible Procession',
        'language': 'Swahili',
        'key_signature': 'G',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Nimesikia Bwana waniita,\n"
            "Sauti yake inaingia moyoni,\n"
            "Najibu: Nitatumika,\n"
            "Ee Bwana, mimi hapa nipo.\n\n"
            "Injili yako ni nuru,\n"
            "Inauongoza moyo wangu,\n"
            "Neno lako ni taa,\n"
            "Katika njia zangu zote.\n\n"
            "Simama na usikie,\n"
            "Bwana anasema kwako,\n"
            "Fungua moyo wako,\n"
            "Upokee neno lake."
        ),
    },
    {
        'title': 'Injili Yake Yesu',
        'category': 'Bible Procession',
        'language': 'Swahili',
        'key_signature': 'D',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Injili yake Yesu,\n"
            "Ni habari njema kwa wote,\n"
            "Tumsikilize Bwana,\n"
            "Anasema maneno ya uzima.\n\n"
            "Utukufu kwako, ee Bwana,\n"
            "Kwa neno lako takatifu,\n"
            "Tunasimama kusikiliza,\n"
            "Maneno ya uzima wa milele.\n\n"
            "Aleluya, Aleluya,\n"
            "Sifa kwa Bwana Yesu,\n"
            "Aleluya, Aleluya,\n"
            "Neno lake ni kweli."
        ),
    },

    # ── ORDINARY — MISA BANANA ────────────────────────────────────────────
    {
        'title': 'Bwana Utuhurumie',
        'category': 'ord-Kyrie',
        'language': 'Swahili',
        'key_signature': 'F',
        'misa_id': 'banana',
        'ord_part': 'Kyrie',
        'lyrics': (
            "Bwana, utuhurumie.\n"
            "Bwana, utuhurumie.\n\n"
            "Kristo, utuhurumie.\n"
            "Kristo, utuhurumie.\n\n"
            "Bwana, utuhurumie.\n"
            "Bwana, utuhurumie."
        ),
    },
    {
        'title': 'Utukufu kwa Mungu',
        'category': 'ord-Gloria',
        'language': 'Swahili',
        'key_signature': 'F',
        'misa_id': 'banana',
        'ord_part': 'Gloria',
        'lyrics': (
            "Utukufu kwa Mungu juu mbinguni,\n"
            "Na amani duniani,\n"
            "Kwa watu wa upendo wake.\n\n"
            "Tunakusifu, tunakuabudu,\n"
            "Tunakutukuza, tunakushukuru,\n"
            "Kwa utukufu wako mkuu.\n\n"
            "Ee Bwana Mungu, Mfalme wa mbinguni,\n"
            "Mungu Baba Mwenyezi,\n"
            "Ee Bwana, Mwana wa pekee, Yesu Kristo.\n\n"
            "Ee Bwana Mungu, Mwanakondoo wa Mungu,\n"
            "Mwana wa Baba,\n"
            "Unaondoa dhambi za ulimwengu — utuhurumie.\n"
            "Unaondoa dhambi za ulimwengu — pokea sala yetu.\n"
            "Uketi mkono wa kuume wa Baba — utuhurumie.\n\n"
            "Kwa kuwa wewe peke yako u Mtakatifu,\n"
            "Wewe peke yako u Bwana,\n"
            "Wewe peke yako u Mtukufu, ee Yesu Kristo,\n"
            "Pamoja na Roho Mtakatifu,\n"
            "Katika utukufu wa Mungu Baba. Amina."
        ),
    },

    # ── ORDINARY — MISA AMECEA ────────────────────────────────────────────
    {
        'title': 'Mtakatifu',
        'category': 'ord-Sanctus',
        'language': 'Swahili',
        'key_signature': 'G',
        'misa_id': 'amecea',
        'ord_part': 'Sanctus',
        'lyrics': (
            "Mtakatifu, Mtakatifu, Mtakatifu,\n"
            "Bwana Mungu wa majeshi.\n"
            "Mbingu na nchi vimejaa utukufu wako.\n\n"
            "Hosanna juu mbinguni.\n"
            "Amebarikiwa anayekuja kwa jina la Bwana.\n"
            "Hosanna juu mbinguni.\n\n"
            "[SATB]\n"
            "S/A: Mtakatifu, Mtakatifu, Mtakatifu\n"
            "T/B: Bwana Mungu wa majeshi\n"
            "Wote: Mbingu na nchi vimejaa utukufu wako\n"
            "Hosanna, Hosanna juu mbinguni."
        ),
    },
    {
        'title': 'Fumbo la Imani',
        'category': 'ord-Other',
        'language': 'Swahili',
        'key_signature': 'G',
        'misa_id': 'amecea',
        'ord_part': 'Mystery of Faith',
        'lyrics': (
            "Fumbo la imani:\n\n"
            "Bwana wetu Yesu Kristo alikufa,\n"
            "Alifufuka kutoka kwa wafu,\n"
            "Na atakuja tena kwa utukufu.\n\n"
            "Tunaona kifo chako, Bwana,\n"
            "Tunaadhimisha ufufuko wako,\n"
            "Tunangojea kuja kwako kwa utukufu.\n\n"
            "Kila wakati tulapo mkate huu,\n"
            "Na kunywa kikombe hiki,\n"
            "Tunatangaza kifo chako, Bwana,\n"
            "Hadi utakapokuja."
        ),
    },
    {
        'title': 'Mwanakondoo wa Mungu',
        'category': 'ord-Agnus Dei',
        'language': 'Swahili',
        'key_signature': 'G',
        'misa_id': 'amecea',
        'ord_part': 'Agnus Dei',
        'lyrics': (
            "Mwanakondoo wa Mungu,\n"
            "Unaondoa dhambi za ulimwengu:\n"
            "Utuhurumie.\n\n"
            "Mwanakondoo wa Mungu,\n"
            "Unaondoa dhambi za ulimwengu:\n"
            "Utuhurumie.\n\n"
            "Mwanakondoo wa Mungu,\n"
            "Unaondoa dhambi za ulimwengu:\n"
            "Utupe amani.\n\n"
            "[SATB]\n"
            "S: Mwanakondoo wa Mungu\n"
            "A: Unaondoa dhambi\n"
            "T: Za ulimwengu\n"
            "B: Utuhurumie / Utupe amani"
        ),
    },
    {
        'title': 'Ishara ya Amani',
        'category': 'ord-Other',
        'language': 'Swahili',
        'key_signature': 'C',
        'misa_id': 'amecea',
        'ord_part': 'Sign of Peace',
        'lyrics': (
            "Ishara ya amani,\n"
            "Tupeaneni amani,\n"
            "Amani ya Bwana,\n"
            "Iwe pamoja nawe.\n\n"
            "Kristo ndiye amani yetu,\n"
            "Amefanya wote kuwa wamoja,\n"
            "Ukuta wa chuki amevunja,\n"
            "Sasa tuko katika amani.\n\n"
            "Nenda kwa ndugu yako,\n"
            "Mpe mkono wa amani,\n"
            "Amani ya Kristo iwe,\n"
            "Mioyoni mwetu sote."
        ),
    },

    # ── OFFERTORY ─────────────────────────────────────────────────────────
    {
        'title': 'Nitatoa Nini',
        'category': 'Offertory',
        'language': 'Swahili',
        'key_signature': 'D',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Nitatoa nini kwa Bwana,\n"
            "Kwa wema wake wote kwangu?\n"
            "Nitainua kikombe cha wokovu,\n"
            "Na kulitaja jina la Bwana.\n\n"
            "Naomba Bwana nikatoe,\n"
            "Moyo wangu na roho yangu,\n"
            "Sadaka yangu ya kweli,\n"
            "Ni maisha yangu yote kwako.\n\n"
            "Ee Bwana, pokea hivi,\n"
            "Matoleo ya mikono yetu,\n"
            "Uibariki sadaka hii,\n"
            "Iwe tamu mbele yako."
        ),
    },
    {
        'title': 'Leteni Ndama Wanono',
        'category': 'Offertory',
        'language': 'Swahili',
        'key_signature': 'G',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Leteni ndama wanono,\n"
            "Tumsherehekee Bwana,\n"
            "Leteni sadaka njema,\n"
            "Kwa Mungu aliyetupenda.\n\n"
            "Leteni, leteni, leteni,\n"
            "Sadaka kwa furaha,\n"
            "Tutoe kwa moyo mkamilifu,\n"
            "Kwa Bwana Mungu wetu.\n\n"
            "Mungu ametutendea wema,\n"
            "Ametupa neema zake,\n"
            "Namshukuru Mungu wangu,\n"
            "Kwa upendo wake wote."
        ),
    },
    {
        'title': 'Twende Wote Tukatoe',
        'category': 'Offertory',
        'language': 'Swahili',
        'key_signature': 'C',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Twende wote tukatoe,\n"
            "Sadaka kwa Mungu wetu,\n"
            "Tutoe kwa furaha,\n"
            "Kwa moyo wa upendo.\n\n"
            "Mkono wa Bwana umeshiba,\n"
            "Yuatupenda sisi sote,\n"
            "Tutoe kwa moyo safi,\n"
            "Kwa Bwana wa mbinguni.\n\n"
            "Sadaka yetu ni ishara,\n"
            "Ya upendo wetu kwake,\n"
            "Tutoe kwa shangwe nyingi,\n"
            "Kwa Bwana Mungu wetu."
        ),
    },
    {
        'title': 'Yamba Yamba Yahweh',
        'category': 'Offertory',
        'language': 'Other',
        'key_signature': 'F',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Yamba yamba Yahweh,\n"
            "Yamba yamba Seigneur,\n"
            "Nous t'offrons nos dons,\n"
            "Accept our offering.\n\n"
            "Yamba yamba Yahweh,\n"
            "Twakupa sadaka zetu,\n"
            "Pokea, ee Bwana,\n"
            "Matoleo ya mikono yetu.\n\n"
            "Yamba, yamba, yamba,\n"
            "Mungu wa nguvu zote,\n"
            "Pokea kwa upole,\n"
            "Sadaka za watoto wako."
        ),
    },
    {
        'title': 'Ngai Niariturathimaga',
        'category': 'Offertory',
        'language': 'Kikuyu',
        'key_signature': 'G',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Ngai niariturathimaga,\n"
            "Nĩtwahotaga wega na mĩgaka,\n"
            "Tũgũcookia ngatho Ngai,\n"
            "Kwa ũteithio wake wote.\n\n"
            "Tũgũriha nini Ngai,\n"
            "Kwa wega wake wote?\n"
            "Tũkamuhe mioyo yetu,\n"
            "Na maisha yetu yote.\n\n"
            "Ngai nĩwe ũteithio witu,\n"
            "Nĩwe mũhonokia witu,\n"
            "Tũmũcookeria ngatho,\n"
            "Kwa siku na usiku wote."
        ),
    },
    {
        'title': 'Malaika wa Bwana Uchukue Sadaka',
        'category': 'Offertory',
        'language': 'Swahili',
        'key_signature': 'D',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Malaika wa Bwana uchukue sadaka,\n"
            "Uipeleke mbele za Mungu,\n"
            "Kama vile moshi wa uvumba,\n"
            "Sadaka zetu zimpendeze.\n\n"
            "Chukua, Bwana, sadaka zetu,\n"
            "Za mikono na mioyo,\n"
            "Uzibariki sadaka hizi,\n"
            "Ziwe tamu mbele yako.\n\n"
            "Neno letu na liende,\n"
            "Mbele za kiti chako,\n"
            "Sala zetu na zipae,\n"
            "Kama uvumba mbele yako."
        ),
    },
    {
        'title': 'Sala Yangu na Ipae',
        'category': 'Offertory',
        'language': 'Swahili',
        'key_signature': 'E',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Sala yangu na ipae,\n"
            "Kama uvumba mbele yako,\n"
            "Kuinua mikono yangu,\n"
            "Kuwe kama sadaka ya jioni.\n\n"
            "Simama, Bwana, penye mlango,\n"
            "Uusikie mwimbo wangu,\n"
            "Nikupe moyo wangu,\n"
            "Na roho yangu yote.\n\n"
            "Pokea maneno ya kinywa changu,\n"
            "Na mawazo ya moyo wangu,\n"
            "Yawe ya kupendeza kwako,\n"
            "Ee Bwana, nguvu zangu."
        ),
    },
    {
        'title': 'Sadaka Yangu',
        'category': 'Offertory',
        'language': 'Swahili',
        'key_signature': 'A',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Sadaka yangu ni ndogo,\n"
            "Kama ya yule mjane maskini,\n"
            "Lakini ninakupa yote,\n"
            "Kila kitu nilichonacho.\n\n"
            "Pokea sadaka hii ndogo,\n"
            "Ee Bwana wa mbinguni,\n"
            "Ninakupa mioyo yangu,\n"
            "Sadaka ya kweli ya upendo.\n\n"
            "Kama vile mkate mdogo,\n"
            "Ulioshiba elfu nyingi,\n"
            "Uibariki sadaka hii,\n"
            "Itumike kwa utukufu wako."
        ),
    },
    {
        'title': 'Hiki Kidogo',
        'category': 'Offertory',
        'language': 'Swahili',
        'key_signature': 'C',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Hiki kidogo nilichonacho,\n"
            "Ninakupa wewe Bwana,\n"
            "Hiki kidogo cha mkate,\n"
            "Na divai hii ndogo.\n\n"
            "Ukibariki, ee Bwana,\n"
            "Vitakuwa vingi,\n"
            "Kama mkate wa Yesu,\n"
            "Ulioshibisha elfu nyingi.\n\n"
            "Ninakupa moyo wangu,\n"
            "Hiki ndicho kidogo changu,\n"
            "Nibariki, ee Bwana,\n"
            "Uwe karibu nami."
        ),
    },

    # ── COMMUNION ─────────────────────────────────────────────────────────
    {
        'title': 'Tujongeeni Mezani',
        'category': 'Communion',
        'language': 'Swahili',
        'key_signature': 'F',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Tujongeeni mezani,\n"
            "Meza ya Bwana wetu,\n"
            "Kula mwili wake mtakatifu,\n"
            "Kunywa damu yake ya thamani.\n\n"
            "Tujongeeni, tujongeeni,\n"
            "Mezani mwa Bwana wetu,\n"
            "Chakula cha milele hapa,\n"
            "Kristo mwenyewe ndiye chakula.\n\n"
            "Njooni, njooni wote,\n"
            "Walioitwa na Bwana,\n"
            "Karamuni kwake leo,\n"
            "Meze kwa furaha na amani."
        ),
    },
    {
        'title': 'Enyi Wakristu Wapenzi Njooni',
        'category': 'Communion',
        'language': 'Swahili',
        'key_signature': 'G',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Enyi Wakristu wapenzi, njooni,\n"
            "Meze mkate wa uzima,\n"
            "Yesu anatualika wote,\n"
            "Kwenye karamu ya upendo.\n\n"
            "Njooni, njooni, njooni wote,\n"
            "Meza ya Bwana imekaa,\n"
            "Tumeze kwa furaha,\n"
            "Mkate wa mbinguni huu.\n\n"
            "Yesu ndiye mkate wetu,\n"
            "Aliotoka mbinguni,\n"
            "Aulaye ataishi milele,\n"
            "Na Bwana Mungu wake."
        ),
    },
    {
        'title': 'Aulaye Mwili Wangu',
        'category': 'Communion',
        'language': 'Swahili',
        'key_signature': 'D',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Aulaye mwili wangu,\n"
            "Na kuinywa damu yangu,\n"
            "Ana uzima wa milele,\n"
            "Nami nitamfufua siku ya mwisho.\n\n"
            "Mimi ndimi mkate wa uzima,\n"
            "Ulishukao kutoka mbinguni,\n"
            "Aulaye mkate huu ataishi,\n"
            "Milele na milele.\n\n"
            "Kama vile Baba alivyo hai,\n"
            "Na akanituma mimi niwe hai,\n"
            "Vivyo hivyo aulaye mimi,\n"
            "Ataishi kwa sababu yangu."
        ),
    },
    {
        'title': 'Kama Ayala',
        'category': 'Communion',
        'language': 'Swahili',
        'key_signature': 'E',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Kama ayala aoneavyo,\n"
            "Mto wa maji safi,\n"
            "Ndivyo roho yangu inavyomtamani,\n"
            "Ee Mungu wa mbinguni.\n\n"
            "Roho yangu imemtamani Mungu,\n"
            "Mungu wa uzima wote,\n"
            "Nitakapofika, nitamwona,\n"
            "Uso wake mtukufu.\n\n"
            "Machozi yangu yamekuwa chakula changu,\n"
            "Usiku na mchana,\n"
            "Watu wanisema, wapi Mungu wako?\n"
            "Lakini moyo wangu unamtumainia."
        ),
    },
    {
        'title': 'Bwana Anakuja',
        'category': 'Communion',
        'language': 'Swahili',
        'key_signature': 'C',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Bwana anakuja, Bwana anakuja,\n"
            "Kwa sura ya mkate na divai,\n"
            "Mwambie habari njema, mwambie,\n"
            "Bwana anakuja kwetu.\n\n"
            "Furahini, furahini sana,\n"
            "Bwana anakuja leo,\n"
            "Fumba mikono, fumba macho,\n"
            "Mpokee kwa furaha.\n\n"
            "Yesu anakuja kwangu,\n"
            "Moyo wangu umefurahi,\n"
            "Nakukaribisha Bwana,\n"
            "Ukae nami milele."
        ),
    },
    {
        'title': 'Yesu Atwirire Niwe',
        'category': 'Communion',
        'language': 'Kikuyu',
        'key_signature': 'G',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Yesu atwirire niwe,\n"
            "Nĩndakũũya mũtĩ wa ũhoro,\n"
            "Nĩndakũũya mũtĩ wa ũhoro,\n"
            "Wega wake nĩ mũnene.\n\n"
            "Nĩwe nyumba yake,\n"
            "Nĩwe mwĩrĩ wake,\n"
            "Yesu atwirire niwe,\n"
            "Nĩkũmwendia na moyo woothe.\n\n"
            "Nĩwe na we hamwe,\n"
            "Ũhoro wake nĩ mwega,\n"
            "Tũkũhũthĩria ũhoro wake,\n"
            "Tũkũmwendia na moyo woothe."
        ),
    },
    {
        'title': 'Thayu wa Kristo',
        'category': 'Communion',
        'language': 'Kikuyu',
        'key_signature': 'F',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Thayu wa Kristo ũgwatire moyo waku,\n"
            "Thayu wake nĩ mwega,\n"
            "Thayu wa Kristo ũgwatire moyo waku,\n"
            "Nĩwe nake ũhoro woothe.\n\n"
            "Kristo nĩ thayu witu,\n"
            "Agĩtũthimĩria wega,\n"
            "Tũmwendia na moyo woothe,\n"
            "Thayu wake nĩ witu.\n\n"
            "Thayu, thayu, thayu wa Kristo,\n"
            "Ũgwatire mĩoyo yitu yothe,\n"
            "Tũkũmwendia na moyo woothe,\n"
            "Kristo nĩ Bwana witu."
        ),
    },

    # ── THANKSGIVING ──────────────────────────────────────────────────────
    {
        'title': 'Neno Asante',
        'category': 'Thanksgiving',
        'language': 'Swahili',
        'key_signature': 'D',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Neno asante, neno asante,\n"
            "Kwa Mungu aliyetupenda,\n"
            "Neno asante, neno asante,\n"
            "Kwa neema zake zote.\n\n"
            "Asante kwa mkate huu,\n"
            "Asante kwa divai hii,\n"
            "Asante kwa mwili na damu,\n"
            "Ya Yesu Kristo Bwana wetu.\n\n"
            "Asante Bwana kwa upendo,\n"
            "Asante kwa wokovu wako,\n"
            "Asante kwa pumzi ya uzima,\n"
            "Asante kwa neema zako."
        ),
    },
    {
        'title': 'Nĩ Thengiũ Mwathani',
        'category': 'Thanksgiving',
        'language': 'Kikuyu',
        'key_signature': 'G',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Nĩ thengiũ Mwathani,\n"
            "Kwa wega waku woothe,\n"
            "Nĩ thengiũ Mwathani,\n"
            "Kwa ũteithio waku.\n\n"
            "Ũnĩrathimĩtie sana,\n"
            "Ũnĩfũmbĩtie wĩra,\n"
            "Nĩ thengiũ sana,\n"
            "Mwathani wangu Ngai.\n\n"
            "Ngai nĩwe mwathani wangu,\n"
            "Nĩwe mũhonokia wangu,\n"
            "Nĩ thengiũ Ngai wangu,\n"
            "Kwa wega wake woothe."
        ),
    },
    {
        'title': 'Baba Asante',
        'category': 'Thanksgiving',
        'language': 'Swahili',
        'key_signature': 'C',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Baba asante, asante Baba,\n"
            "Kwa upendo wako mkubwa,\n"
            "Baba asante, asante Baba,\n"
            "Kwa zawadi zako zote.\n\n"
            "Umeweza kunilisha,\n"
            "Umeweza kunibusu,\n"
            "Baba asante, asante Baba,\n"
            "Kwa upendo wako wote.\n\n"
            "Asante kwa siku ya leo,\n"
            "Asante kwa nguvu za mwili,\n"
            "Asante kwa pumzi ya uzima,\n"
            "Asante Baba wa mbinguni."
        ),
    },
    {
        'title': 'Ningukugooca we Mwathani',
        'category': 'Thanksgiving',
        'language': 'Kikuyu',
        'key_signature': 'D',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Ningukugooca we Mwathani,\n"
            "Kwa ngatho nene sana,\n"
            "Wega waku nĩ mũnene,\n"
            "Ũndĩrathimĩtie sana.\n\n"
            "Moyo wangu ũkũgooca,\n"
            "Ũkũruta ngatho,\n"
            "Ningukugooca we Mwathani,\n"
            "Ũhoro waku nĩ mwega.\n\n"
            "Ngatho na ngatho na ngatho,\n"
            "Kwa Ngai Mwathani wangu,\n"
            "Ũnĩheete wega na mĩgaka,\n"
            "Ningukugooca siku ciothe."
        ),
    },
    {
        'title': 'Igicokagirie Ngai Ngatho',
        'category': 'Thanksgiving',
        'language': 'Kikuyu',
        'key_signature': 'F',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Igicokagirie Ngai ngatho,\n"
            "Kwa wega wake woothe,\n"
            "Igicokagirie Ngai ngatho,\n"
            "Nĩ we mwene ũhoro.\n\n"
            "Ngatho na ngatho na ngatho,\n"
            "Kwa Ngai witu mwega,\n"
            "Tũmûthaithie tũgĩe,\n"
            "Na ngatho ciake ciothe.\n\n"
            "Tũkũcookeria ngatho,\n"
            "Kwa siku na usiku wote,\n"
            "Ngai nĩ mwega, Ngai nĩ mwega,\n"
            "Tũmũthime na moyo woothe."
        ),
    },

    # ── RECESSIONAL ───────────────────────────────────────────────────────
    {
        'title': 'Ni Nyota',
        'category': 'Recessional',
        'language': 'Swahili',
        'key_signature': 'G',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Ni nyota, ni nyota ya asubuhi,\n"
            "Maria Mama wa Mungu,\n"
            "Ni nyota, ni nyota inayoongoza,\n"
            "Tunakuja kwako Mama.\n\n"
            "Ave Maria, Ave Maria,\n"
            "Mke wa Bwana mkuu,\n"
            "Tunahitaji msaada wako,\n"
            "Mama wa huruma yote.\n\n"
            "Tuombee, ee Mama Maria,\n"
            "Sisi watoto wako,\n"
            "Sasa na saa ya mauti yetu,\n"
            "Uwe karibu nasi."
        ),
    },
    {
        'title': 'Ni Moja / Mkatoliki Simama',
        'category': 'Recessional',
        'language': 'Swahili',
        'key_signature': 'C',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Ni moja, ni moja, tunakwenda pamoja,\n"
            "Katika imani ya Kristo,\n"
            "Ni moja, ni moja, Kanisa moja,\n"
            "Kanisa la Yesu Kristo.\n\n"
            "Mkatoliki simama imara,\n"
            "Katika imani yako,\n"
            "Ushike msalaba wa Kristo,\n"
            "Uwe shahidi wake.\n\n"
            "Nenda na amani ya Bwana,\n"
            "Ipeleke kwa wengine,\n"
            "Umsifu Mungu wetu,\n"
            "Katika maisha yako yote."
        ),
    },
    {
        'title': 'Rũkũngũ Nĩrũmbũke',
        'category': 'Recessional',
        'language': 'Kikuyu',
        'key_signature': 'D',
        'misa_id': '',
        'ord_part': '',
        'lyrics': (
            "Rũkũngũ nĩrũmbũke,\n"
            "Maria Mama wa Ngai,\n"
            "Rũkũngũ nĩrũmbũke,\n"
            "Mama wa ũteithio.\n\n"
            "Tũkũrorire, Mama Maria,\n"
            "Ũtũteithie ciothe,\n"
            "Rũkũngũ nĩrũmbũke,\n"
            "Njĩra yothe tũhehũke.\n\n"
            "Ave Maria, Mama mwega,\n"
            "Tũtũĩre thĩ no twega,\n"
            "Tũkũhoya, Mama Maria,\n"
            "Ũtũhonokia ciothe."
        ),
    },
]


class Command(BaseCommand):
    help = 'Seed the database with the parish song catalogue and default admin users.'

    def handle(self, *args, **options) -> None:
        self.stdout.write(self.style.MIGRATE_HEADING('Parish Songs — Seeding database…'))

        # ── Create superadmin ──────────────────────────────────────────────
        superadmin, created = User.objects.get_or_create(
            username='director',
            defaults={
                'email': 'director@parish.org',
                'first_name': 'Choir',
                'last_name': 'Director',
                'role': 'superadmin',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            superadmin.set_password('ChangeMe123!')
            superadmin.save()
            self.stdout.write(
                self.style.SUCCESS(
                    '  Created superadmin → username: director  password: ChangeMe123!'
                )
            )
        else:
            self.stdout.write('  Superadmin "director" already exists — skipping.')

        # ── Seed songs ────────────────────────────────────────────────────
        created_count = 0
        skipped_count = 0

        for data in SONGS:
            defaults = {k: v for k, v in data.items() if k != 'title'}
            defaults['uploaded_by'] = superadmin
            defaults['uploaded_by_name'] = 'Choir Director'

            _song, was_created = Song.objects.get_or_create(
                title=data['title'],
                category=data['category'],
                defaults=defaults,
            )
            if was_created:
                created_count += 1
            else:
                skipped_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'  Songs created: {created_count}  |  already existed: {skipped_count}'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'  Total songs in database: {Song.objects.count()}'
            )
        )
        self.stdout.write(self.style.MIGRATE_HEADING('Done. ✓'))

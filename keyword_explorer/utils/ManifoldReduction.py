#import umap
import re
import ast
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from typing import List, Pattern

class EmbeddedText:
    raw_str:str
    source:str
    text:str
    original:List
    reduced:List
    vis_dim:List

    def __init__(self, raw_str:str):
        self.raw_str = raw_str
        self.source_regex = re.compile(r"\w+-\w+-\w+-\d+:")
        self.parse()

    def parse(self):
        # print("parsing {}".format(self.raw_str))
        split_list = self.raw_str.split(":")
        self.source = split_list[0]
        list_str = split_list[1]
        # print(self.source)
        self.original = ast.literal_eval(list_str)
        # for v in self.original:
        #     print(v)

class ManifoldReduction:
    target_dim:int
    embedding_list:List

    def __init__(self, dim:int = 2):
        print("ManifoldReduction.__init__()")
        self.target_dim:int = min(dim, 3)
        self.clear()

    def clear(self):
        self.embedding_list = []

    def load_row(self, row_str:str):
        et = EmbeddedText(row_str)
        self.embedding_list.append(et)

    def calc_embeding(self, perplexity:int = 15):
        mat = []
        et:EmbeddedText
        for et in self.embedding_list:
            mat.append(et.original)
        tsne = TSNE(n_components=self.target_dim, perplexity=perplexity, random_state=42, init='random', learning_rate=200)
        reduced_list = tsne.fit_transform(mat)
        for i in range(len(reduced_list)):
            et = self.embedding_list[i]
            et.reduced = reduced_list[i]
        print("ManifoldReduction.calc_embedding: Finished reduction to {} dimensions".format(self.target_dim))

        # tsne = TSNE(n_components=2, perplexity=15, random_state=42, init='random', learning_rate=200)
        # reduced_list = tsne.fit_transform(mat)
        # for i in range(len(reduced_list)):
        #     et = self.embedding_list[i]
        #     et.vis_dim = reduced_list[i]
        # print("ManifoldReduction.calc_embedding: Finished reduction to 2 dimensions")

    def plot_reduced(self, axs, title:str = None):
        et:EmbeddedText
        x = []
        y = []
        for et in self.embedding_list:
            x.append(et.reduced[0])
            y.append(et.reduced[1])
        if title != None:
            axs.title.set_text(title)
        axs.scatter(x, y, s=2, c="blue")

def main():
    # s = '''text-similarity-ada-001:[-0.011615040712058544, 0.011625140905380249, 0.0046712663024663925, 0.05179298296570778, 0.024704687297344208, -0.010847438126802444, 0.026381291449069977, -0.003971838857978582, 0.056681398302316666, 0.03702672943472862, -0.0011110039195045829, -0.0026941844262182713, 0.0019682443235069513, -0.01141303963959217, 0.0014544051373377442, -0.033754318952560425, 0.026542892679572105, 0.024926887825131416, 0.017594261094927788, 0.028179097920656204, 0.024947086349129677, 0.014119849540293217, -0.010433336719870567, 0.011332239955663681, 0.05437859147787094, 0.012109942734241486, 0.016564058139920235, 0.02613889053463936, 0.013675447553396225, -0.04553095996379852, -0.05284338444471359, -0.014079449698328972, -0.012685644440352917, 0.05494419112801552, 0.04912657290697098, 0.00046523287892341614, -0.0319565124809742, 0.0170589592307806, -0.024785486981272697, 0.0050373924896121025, -0.046783365309238434, -0.014554151333868504, 0.00676702382043004, -0.019644569605588913, -0.02741149626672268, 0.004196564666926861, -0.07983067631721497, -0.0371883288025856, -0.02864369936287403, 0.019018366932868958, -0.053812988102436066, 0.04149094596505165, -0.02745189517736435, 0.03296651691198349, 0.005822670180350542, -0.05033857747912407, 0.02581568993628025, -0.005272218491882086, -0.02137167565524578, 0.005706519819796085, -0.01727106049656868, -0.02585609070956707, 0.006974074523895979, -0.030744507908821106, -0.032279711216688156, -0.0014316800516098738, -0.01744276098906994, -0.035127922892570496, -0.03276451304554939, 0.011342339217662811, 0.014735951088368893, 0.01430165022611618, -0.01723065972328186, -0.010968638584017754, -0.008074978366494179, -0.0057469201274216175, 0.0009727596770972013, -0.007731576915830374, 0.012029142118990421, 0.005060117691755295, 0.008337578736245632, 0.00644887238740921, 0.002261145506054163, -0.023613883182406425, 0.004065264016389847, 0.03343111649155617, 0.010059635154902935, -0.019775869324803352, 0.009660683572292328, 0.014028948731720448, -0.0014468301087617874, -0.00791842769831419, -0.020765673369169235, -0.015301553532481194, 0.01146353967487812, -0.005772170145064592, 0.0017662437167018652, 0.02173527516424656, 0.020452572032809258, 0.02587629109621048, -0.004562690854072571, 0.0013925423845648766, -0.06569062918424606, -0.039369937032461166, 0.01594795659184456, 0.003694087965413928, -0.0021184824872761965, -0.02177567593753338, 0.006166071631014347, -0.019513268023729324, 0.023250281810760498, 0.036622729152441025, 0.013433046638965607, -0.023432081565260887, 0.049530573189258575, 0.04068294167518616, 0.0005261487094685435, 0.022078678011894226, -0.001020103576593101, 0.06851863861083984, -0.008332529105246067, -0.017947763204574585, 0.08168908208608627, -0.03023950569331646, 0.010998938232660294, -0.010877737775444984, -0.007090224884450436, 0.02565409056842327, -0.011827141046524048, -0.01511975284665823, -0.01141303963959217, -0.008352729491889477, 0.005181318148970604, -0.00435059005394578, 0.025391489267349243, -0.03207771107554436, -0.01438244991004467, 0.032279711216688156, 0.027977097779512405, -0.02454308606684208, 0.0021083822939544916, 0.014937952160835266, -0.016119657084345818, -0.012746244668960571, 0.014119849540293217, 0.01506925281137228, -0.017776062712073326, -0.013907748274505138, 0.027896298095583916, -0.01160494051873684, 0.012554343789815903, -0.00756997661665082, 0.03607732802629471, 0.03890533745288849, 0.006812473759055138, 0.014867251738905907, -0.01225134264677763, -0.043995752930641174, 0.019715268164873123, -0.008559780195355415, -0.03258271515369415, -0.0006214677705429494, -0.06318581849336624, 0.03456231951713562, -0.006155971437692642, 0.0019606694113463163, -0.020785871893167496, 0.026967095211148262, 0.024926887825131416, -0.03771353140473366, -0.02426028437912464, 0.0170589592307806, 0.002252307953312993, -0.014887452125549316, 0.003676412859931588, -0.0036890378687530756, 0.004098089411854744, -0.02165447548031807, -0.008625430054962635, 0.012574544176459312, 0.0005908520543016493, -0.001134360209107399, -0.008857730776071548, 0.010756537318229675, 0.023836083710193634, -0.0017056434880942106, 0.052318181842565536, 0.004585416056215763, -0.026967095211148262, -0.014665251597762108, 0.007044774480164051, -0.030421307310461998, 0.0374913327395916, 0.014261249452829361, 0.01730136014521122, 0.0021576201543211937, 0.02014956995844841, -0.02856289967894554, 0.00022314765374176204, 0.0061054714024066925, -0.0013092170702293515, -0.0017233184771612287, -0.004156164359301329, 0.011796841397881508, -0.011362539604306221, 0.0009948534425348043, -0.00924658216536045, -0.007691177073866129, -0.010706037282943726, 0.02179587632417679, 0.015321753919124603, -0.0651654303073883, 0.01888706535100937, 0.0007189962780103087, 0.016685258597135544, -0.028239699080586433, -0.028138699010014534, -0.049772974103689194, 0.05041937530040741, 0.03910733759403229, 0.011261539533734322, -0.019836468622088432, -0.005807520356029272, -0.028522498905658722, 0.019846569746732712, -0.023896683007478714, -0.0006823836592957377, 0.006373122334480286, 0.026179291307926178, -0.0010756537085399032, 0.06464022397994995, 0.00021888670744374394, -0.019432468339800835, 0.005342918913811445, 0.009802084416151047, -0.04326855018734932, 0.04601576179265976, 0.04553095996379852, 0.06459982693195343, 0.011544340290129185, 0.016493357717990875, -0.0073932260274887085, -0.010302036069333553, 0.02731049619615078, 0.002848210046067834, 0.0031638359650969505, 0.029350703582167625, 0.017816461622714996, 0.02757309563457966, 0.0316535122692585, 0.008337578736245632, 0.0028810349758714437, 0.04722776636481285, -0.02169487625360489, -0.003545112442225218, 0.02593689039349556, -0.038359932601451874, -0.01209984254091978, 0.04326855018734932, 0.01882646605372429, -3.6814826671616174e-06, 0.033855319023132324, -0.019422367215156555, -0.015240953303873539, -0.012726044282317162, 0.029875904321670532, -0.01603885553777218, 0.03702672943472862, 0.01565505564212799, -0.006307472009211779, 0.027633696794509888, 0.039773937314748764, -0.02025057002902031, -0.02302808128297329, 0.04431895539164543, -0.02597729116678238, 0.04136974364519119, -0.02882550098001957, -0.01569545455276966, 0.007928527891635895, -0.04031934216618538, 0.03021930530667305, -0.023856284096837044, -0.007923477329313755, 0.01887696608901024, -0.003237061435356736, 0.0010365161579102278, -0.028259899467229843, -0.009362732991576195, 0.03848113492131233, 0.013180546462535858, -0.021210074424743652, 0.011837241239845753, -0.3493804335594177, 0.012049342505633831, -0.019291067495942116, 0.03335031494498253, -0.004762166645377874, -0.0019429943058639765, -0.0021853952202945948, -0.011615040712058544, 0.0313505083322525, 0.008095178753137589, 0.007575026713311672, -0.006797323934733868, 0.026522692292928696, -0.018442664295434952, 0.02587629109621048, 0.014907652512192726, -0.03318871557712555, 0.005019717384129763, -0.030764708295464516, 0.006630673073232174, -0.014685451053082943, 0.0003916919813491404, -0.019392067566514015, -0.02724989503622055, -0.04924777150154114, 0.008751681074500084, 0.03139090910553932, 0.048076167702674866, -0.006792273838073015, 0.03894573450088501, -0.027653897181153297, -0.0069841742515563965, 0.023250281810760498, 0.06060021370649338, 0.017695261165499687, 0.010251536034047604, 0.030421307310461998, -0.04306655004620552, -0.00017801312787923962, -0.023411881178617477, -0.049611374735832214, -0.035390522330999374, 0.05215658247470856, -0.010271735489368439, -0.017967963591217995, 0.004653591196984053, -0.016907459124922752, -0.029593102633953094, 0.04025873914361, 0.02157367579638958, 0.0050222426652908325, -0.04734896495938301, 0.025553088635206223, -0.03264331445097923, -0.008428479544818401, 0.05292418599128723, 0.03191611170768738, 0.0067417738027870655, 0.018291164189577103, 0.012857344932854176, 0.02743169665336609, 0.0489649698138237, 0.02599749155342579, -0.040884941816329956, 0.005822670180350542, -0.007913378067314625, -0.03141111135482788, 0.0542977899312973, -0.010074784979224205, 0.07841667532920837, -0.004186464473605156, -0.00538331875577569, 0.04864177107810974, -0.0011779166525229812, 0.0025224839337170124, -0.0483589693903923, -0.004979317542165518, -0.026664093136787415, 0.0073275757022202015, 0.009650583378970623, -0.019493067637085915, -0.02882550098001957, 0.02589649148285389, 0.009903084486722946, 0.04013754054903984, -0.029471902176737785, 0.011564540676772594, 0.0015591928968206048, -0.00580247025936842, -0.024805687367916107, -0.02292707934975624, 0.023856284096837044, -0.009276882745325565, 0.019695069640874863, -0.02848209999501705, 0.02039197087287903, 0.026906494051218033, 0.011655440554022789, 0.005635819863528013, 0.013311846181750298, -0.0074083758518099785, 0.03747113049030304, 0.003668837947770953, -0.05272218585014343, 0.004706616513431072, 0.019826369360089302, -0.04799536615610123, -0.02464408613741398, -0.0173114612698555, -0.029411302879452705, 0.004764691460877657, 0.0027042843867093325, -0.00436826515942812, -0.042581748217344284, 0.01522075291723013, 0.05066177621483803, 0.001753618591465056, 0.025391489267349243, -0.01706906035542488, -0.01430165022611618, -0.06060021370649338, -0.029128501191735268, 0.008357779122889042, -0.002232107799500227, -0.02426028437912464, 0.008574930019676685, -0.018988067284226418, 0.03833973407745361, 0.026926694437861443, 0.019361767917871475, 0.05159097909927368, 0.04496535658836365, -0.035208724439144135, 0.0037774131633341312, -0.02704789489507675, -0.008105278015136719, -0.046742964535951614, -0.006327671930193901, -0.018382064998149872, 0.03466331958770752, 0.04149094596505165, 0.019785968586802483, -0.027674097567796707, 0.04298574849963188, -0.02173527516424656, 0.058257002383470535, 0.04860137030482292, 0.006044871173799038, 0.02603789046406746, -0.014564250595867634, 0.008261828683316708, 0.03589552640914917, 0.017947763204574585, -0.029189102351665497, 0.020907072350382805, -0.012604843825101852, -0.013554247096180916, 0.03343111649155617, -0.01015558559447527, -0.002056619618088007, 0.030663706362247467, -0.002167720114812255, -0.006721573416143656, 0.031047508120536804, -0.037895333021879196, 0.023977484554052353, -0.04601576179265976, 0.0041511147283017635, 0.022401878610253334, 0.004792466759681702, -0.007999228313565254, -0.0639130249619484, 0.004610666073858738, 0.016685258597135544, 0.00033740431535989046, 0.014715751633048058, 0.007822477258741856, -0.011564540676772594, 0.012261442840099335, 0.009993985295295715, -0.009180932305753231, 0.012039242312312126, -0.002110907342284918, 0.0034491620026528835, 0.010897938162088394, -0.010296986438333988, 0.025310687720775604, -0.01375624816864729, 0.013180546462535858, 0.021917076781392097, 0.011372639797627926, -0.007357875816524029, -0.04702576622366905, -0.016402456909418106, -0.01286744512617588, 0.025431888177990913, 0.022199878469109535, 0.03458252176642418, -0.04492495581507683, -0.030401106923818588, -0.009120332077145576, 0.02563389018177986, -0.01365524809807539, 0.03306751698255539, 0.01718015968799591, 0.0009525595814920962, -0.09081951528787613, -0.015180353075265884, -0.04078394174575806, 0.01719026081264019, 0.038036733865737915, 0.010463636368513107, 0.024906687438488007, -0.01150394044816494, -0.02866389974951744, 4.0400140278507024e-05, 0.004885891918092966, 0.0018318939255550504, 0.021028272807598114, 0.04726816713809967, 0.02858310006558895, -0.0025666714645922184, 0.008625430054962635, 0.01438244991004467, 0.00716597493737936, 0.015240953303873539, 0.02593689039349556, 0.02753269672393799, -0.011867541819810867, -0.01704885996878147, -0.03488552197813988, -0.029451703652739525, 0.028138699010014534, 0.03716813027858734, 0.010029335506260395, -0.01855376549065113, -0.035148121416568756, -0.011271639727056026, 0.0313505083322525, 0.00036644190549850464, 0.029047701507806778, 6.714945629937574e-05, -0.04460175707936287, 0.018169963732361794, 0.015614654868841171, 0.012281643226742744, -0.009241532534360886, 0.03419872000813484, -0.0018154813442379236, -0.013140145689249039, -0.013917848467826843, 0.02450268529355526, 0.0016980684595182538, -0.006681173574179411, -0.01862446591258049, -0.004800041671842337, -0.0016942808870226145, 0.02575509063899517, 0.017715461552143097, 0.023694682866334915, -0.02434108592569828, -0.029774904251098633, 0.012685644440352917, 0.016341857612133026, 0.02135147526860237, -0.007711376994848251, 0.02022027038037777, 0.009928334504365921, -0.06334742158651352, -0.009004181250929832, -0.01574595458805561, 0.028158899396657944, -0.010463636368513107, 0.05292418599128723, 0.024058284237980843, -0.1874566525220871, 0.03284531459212303, -0.0375923328101635, -0.013463347218930721, -0.05187378078699112, -0.026260090991854668, 0.013544147834181786, -0.02448248490691185, 0.004398565273731947, -0.05740860104560852, 0.013968348503112793, -0.045288559049367905, -0.00866582989692688, 0.045450158417224884, -0.036481328308582306, -0.014645051211118698, -0.026987293735146523, -0.05126778036355972, -0.02589649148285389, 0.027795298025012016, -0.00940313283354044, 0.030825307592749596, 0.010115185752511024, 0.012332143262028694, 0.029269902035593987, 0.011180738918483257, -0.015614654868841171, 0.05021737515926361, -0.0065296730026602745, 0.017978062853217125, -0.025088487192988396, 0.00872138049453497, 0.014988452196121216, -0.017937662079930305, -0.007302325684577227, 0.02033137157559395, -0.05033857747912407, 0.017755862325429916, -0.02714889496564865, -0.022624079138040543, -0.00043303900747559965, -0.03880433738231659, 0.006615523248910904, 0.022098876535892487, 0.02436128444969654, -0.011423139832913876, 0.04294535145163536, -0.02613889053463936, -0.0022762955632060766, 0.03775393217802048, -0.048197370022535324, 0.0037622631061822176, -0.02462388575077057, 0.027977097779512405, -0.01851336471736431, -0.053974587470293045, 0.023310881108045578, 0.0404607430100441, 0.029310302808880806, 0.02151307463645935, 0.10051555186510086, 0.005640869960188866, -0.03304731473326683, 0.03872353583574295, 0.009241532534360886, 0.016836758702993393, 0.023694682866334915, -0.002608334179967642, -0.05328778550028801, 0.0032749364618211985, -0.007221525069326162, 0.017675062641501427, 0.01370574813336134, -0.013099745847284794, -0.01232204306870699, -0.018260864540934563, 0.04197574779391289, 0.03791553154587746, -0.014140048995614052, -0.012625044211745262, -0.02133127488195896, 0.019624369218945503, 0.020129369571805, 0.022038277238607407, -0.0005021611577831209, 0.035127922892570496, -0.016806459054350853, 0.018180062994360924, -0.09469792991876602, 0.010291935876011848, -0.01361484732478857, 0.03446131944656372, 0.042500950396060944, -0.01889716647565365, -0.01450365036725998, 0.005570169538259506, -0.03159290924668312, -0.016786258667707443, 0.03157271072268486, -0.0013761298032477498, -0.015291453339159489, 0.016877159476280212, -0.0006918524159118533, 0.04165254533290863, -0.003333011642098427, 0.019472867250442505, 0.04839937016367912, -0.009685933589935303, 0.01580655574798584, 0.0028078097384423018, -0.018361864611506462, 0.046904563903808594, 0.013463347218930721, -0.022725079208612442, 0.023270482197403908, 0.017584161832928658, 0.022502878680825233, -0.06318581849336624, -0.017604362219572067, -0.015513653866946697, -0.019381968304514885, 0.020886873826384544, 0.01854366436600685, 0.0010226286249235272, -0.009463733062148094, -0.00107123504858464, 0.012362442910671234, -0.050782978534698486, 0.036440927535295486, -0.031087908893823624, -0.013978448696434498, 0.030603107064962387, 0.03827913478016853, 0.013816848397254944, -0.007746727205812931, -0.02575509063899517, -0.009256682358682156, 0.009458683431148529, -0.022038277238607407, -0.011817041784524918, 0.004555115941911936, 0.00646907277405262, 0.042177747935056686, 0.008625430054962635, 0.03821853548288345, 0.012978545390069485, 0.011362539604306221, 0.002214432694017887, -0.011776641011238098, 0.010180835612118244, -0.0020061195828020573, -0.005918620619922876, -0.00580247025936842, 0.02729029580950737, 0.016210556030273438, -0.028219498693943024, 0.0037723632995039225, 0.036764129996299744, 0.0319565124809742, -0.010276786051690578, 0.011150439269840717, -0.02157367579638958, -0.015564154833555222, -0.02304827980697155, 0.031148508191108704, 0.0019871818367391825, 0.015059152618050575, -0.013544147834181786, -0.023836083710193634, 0.02601769007742405, -0.02900730073451996, 0.039309337735176086, -0.004047589376568794, 0.02029097080230713, 0.02858310006558895, -0.02577529102563858, -0.005065167788416147, 0.020947473123669624, -0.027916498482227325, -0.029411302879452705, 0.02137167565524578, 0.01071613747626543, 0.04197574779391289, 0.000482276693219319, -0.003989513963460922, 0.019644569605588913, -0.00604992127045989, 0.02165447548031807, 0.008792080916464329, -0.042541347444057465, -0.01866486482322216, 0.05607539787888527, 0.003186561167240143, -0.0023242705501616, -0.0025502589996904135, -0.01006973534822464, -0.019482968375086784, -0.016594357788562775, 0.025431888177990913, -0.006792273838073015, -0.02025057002902031, 0.006322622299194336, -0.04706616327166557, 0.020503072068095207, 0.019139567390084267, 0.024724885821342468, 0.013988548889756203, -0.0099636847153306, -0.03876393660902977, -0.049732573330402374, 0.013948149047791958, 0.009741484187543392, 0.04565215855836868, 0.01375624816864729, 0.006181221455335617, -0.002506071235984564, 0.02585609070956707, 0.03908713534474373, 0.03288571536540985, 0.03023950569331646, 0.04074354097247124, 0.040884941816329956, -0.01594795659184456, -0.017796263098716736, 0.0013079545460641384, -0.020785871893167496, 0.02031117118895054, -0.031229309737682343, 0.03339071571826935, 0.018038664013147354, 0.016119657084345818, 0.03262311592698097, -0.022098876535892487, 0.01881636492908001, -0.04355135187506676, -0.02886590175330639, -0.016452956944704056, 0.009009231813251972, -0.061327412724494934, -0.02743169665336609, 0.016887258738279343, -0.01155444048345089, -0.02175547555088997, -0.042298946529626846, 0.004805091768503189, -0.014261249452829361, 0.04213734716176987, 0.03405731916427612, -0.00428494019433856, 0.008978931233286858, 0.008938531391322613, -0.024139083921909332, -0.042500950396060944, 0.023836083710193634, -0.004643491469323635, 0.0033001864794641733, 0.008181028999388218, -0.013332046568393707, 0.039571937173604965, 0.016735758632421494, 0.028360899537801743, 0.04347055032849312, -0.01743266172707081, -0.012463443912565708, 0.020886873826384544, -0.03617832809686661, 0.06920544058084488, -0.04593496024608612, -0.005544919520616531, -0.029168901965022087, -0.004888417199254036, 0.02587629109621048, 0.052318181842565536, -0.0200283695012331, -0.01895776577293873, -0.015523754060268402, 0.005292418412864208, 0.016564058139920235, -0.011857441626489162, -0.008776931092143059, 0.010594937019050121, 0.02280587889254093, -0.010261636227369308, 0.027896298095583916, -0.04407655447721481, -0.002994660520926118, -0.013978448696434498, -0.0017005933914333582, 0.0489649698138237, 0.02712869457900524, -0.043914955109357834, -0.027956897392868996, -0.015584354288876057, 0.011988742277026176, -0.02745189517736435, 0.00998388510197401, 0.003471887204796076, -0.028441699221730232, 0.00024318991927430034, 0.04003654047846794, 0.01146353967487812, -0.004577841144055128, -0.00043682652176357806, -0.01867496594786644, 0.007691177073866129, 0.008271928876638412, 0.020523272454738617, 0.013200745917856693, -0.09025391936302185, -0.006979124620556831, -0.047954969108104706, 0.004749541636556387, -0.1155444011092186, 0.04359175264835358, -0.02464408613741398, -0.0012044291943311691, 0.0008913280908018351, 0.005443918984383345, 0.006660973187536001, -0.0516313798725605, -0.023351281881332397, -0.023937083780765533, 0.018311364576220512, -0.03324931487441063, 0.01005458552390337, -0.035370323807001114, -0.0018861816497519612, 0.022442279383540154, 0.005509569309651852, -0.021210074424743652, -0.03480472043156624, 0.0460965596139431, -0.025007687509059906, -0.022199878469109535, -0.017654862254858017, -0.02419968508183956, 0.035168323665857315, -7.827527588233352e-05, 0.03264331445097923, -0.01736196130514145, 0.016735758632421494, 0.06694303452968597, 0.013463347218930721, 0.032138314098119736, 0.04334935173392296, 0.009756634011864662, 0.02735089510679245, 0.0430261492729187, -0.010706037282943726, 0.010918138548731804, 0.0184931643307209, -0.1147364005446434, 0.011847341433167458, -0.013776448555290699, -0.007160924840718508, 0.041066743433475494, -0.0022308453917503357, -0.02460368536412716, -0.2538744807243347, -0.02454308606684208, 0.008484029211103916, -0.0009209969430230558, 0.03627932816743851, 0.04334935173392296, 0.011564540676772594, 0.013079545460641384, -0.02599749155342579, -0.0006363022257573903, 0.04128894582390785, -0.015281353145837784, 0.01143324002623558, 0.0398547388613224, -0.023856284096837044, -0.009872784838080406, 0.033713918179273605, -0.00858503021299839, -0.03902653604745865, -0.018382064998149872, 0.03262311592698097, 0.036602526903152466, 0.02308868058025837, 0.017594261094927788, -0.045490559190511703, -0.046783365309238434, -0.001681655878201127, -0.012837144546210766, 0.022381678223609924, 0.0349259227514267, 0.019371867179870605, 0.07882067561149597, -0.0015945431077852845, -0.03902653604745865, -0.042258549481630325, -0.029148701578378677, 0.016897359862923622, 0.023411881178617477, 0.002277557970955968, -0.02438148483633995, -0.014897552318871021, 0.05013657361268997, -0.007206375245004892, -0.011705940589308739, 0.016069157049059868, 0.02751249633729458, -0.04149094596505165, -0.026502491906285286, -0.023553282022476196, -0.04213734716176987, 0.02034147083759308, -0.17646782100200653, -0.0066761234775185585, -0.019725369289517403, 0.04912657290697098, 0.05421698838472366, 0.014129949733614922, 0.011200939305126667, -0.005262118298560381, -0.03030010685324669, -0.015432854183018208, -0.03403712064027786, 0.01581665500998497, -0.009110231883823872, -0.0023116455413401127, -0.0017233184771612287, -0.03904673829674721, -0.0039693140424788, 0.008489079773426056, -0.03706713020801544, -0.025250088423490524, 0.02320988103747368, 0.015180353075265884, -0.008074978366494179, -0.05025777593255043, 0.002610859228298068, -0.030522307381033897, 0.004552591126412153, -0.018109362572431564, -0.007438675966113806, 0.03621872514486313, 0.02037177048623562, 0.006287272088229656, 0.01145344041287899, 0.02033137157559395, -0.02135147526860237, 0.004191514570266008, -0.014089548960328102, -0.026926694437861443, 0.02601769007742405, 0.056923799216747284, 0.006706423591822386, -0.03328971564769745, 0.022159477695822716, 0.03044150583446026, 0.07179105281829834, 0.026199491694569588, -0.014180449768900871]'''
    # et = EmbeddedText(s)
    num_rows = 100
    mr:ManifoldReduction = ManifoldReduction(2)
    for scalar in [1, 10, 200]:
        print("creating data set [{}]".format(scalar))
        for i in range(num_rows):
            l = np.random.rand(100) *  scalar
            row_str = "random_synthesized:{}".format( ', '.join(map(str,l)))
            # print(row_str)
            mr.load_row(row_str)
    print("Calculating new manifold")

    fig, axs = plt.subplots(2, 3)
    i = 0
    for perplexity in [5, 10, 15, 20, 40, 60]:
        mr.calc_embeding(perplexity=perplexity)
        print("Plotting")
        row = int(i/3)
        col = i%3
        mr.plot_reduced(axs[row][col], "perplex = {}".format(perplexity))
        i += 1
    plt.show()

if __name__ == "__main__":
    #tsne_main()
    main()

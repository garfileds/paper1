# -*- coding: utf-8 -*-
import sys
sys.path.append("..")

import math
import re

from adoug.shannoEntroy import *
from adoug.witness import *
import adoug.tools as tools

regionMap = dict({
	'e0103': {
		2: [-10000, 0.997469231380133, 0.999298993399275, 1.00070100660073, 1.00253076861987, 10000],
		3: [-10000, 0.996624935006418, 0.998048277570157, 0.998924691896633, 0.999653916493858, 1.00034608350614, 1.00107530810337, 1.00195172242984, 1.00337506499358, 10000],
		4: [-10000, 0.995901990381263, 0.997100376025922, 0.99777802168703, 0.998291872127767, 0.998725909243104, 0.999115049856287, 0.999478155359476, 0.999827492692496, 1.0001725073075, 1.00052184464052, 1.00088495014371, 1.0012740907569, 1.00170812787223, 1.00222197831297, 1.00289962397408, 1.00409800961874, 10000],
		5: [-10000, 0.995261476427914, 0.996312932609881, 0.996880846441316, 0.99729431074054, 0.997629465753688, 0.99791708013627, 0.99817287606795, 0.998406068356308, 0.998622582172832, 0.998826498646266, 0.999020787645031, 0.999207714238062, 0.999389081032392, 0.999566382014552, 0.999740906281006, 0.999913812611895, 1.00008618738811, 1.00025909371899, 1.00043361798545, 1.00061091896761, 1.00079228576194, 1.00097921235497, 1.00117350135373, 1.00137741782717, 1.00159393164369, 1.00182712393205, 1.00208291986373, 1.00237053424631, 1.00270568925946, 1.00311915355868, 1.00368706739012, 1.00473852357209, 10000]
	},

	'e0108': {
		2: [-10000, 1.0507, 1.1021, 1.1415, 1.193, 10000],
		3: [-10000, 1.0269, 1.0669, 1.0916, 1.1121, 1.1315, 1.152, 1.1767, 1.2167, 10000],
		4: [-10000, 1.0066, 1.0403, 1.0593, 1.0738, 1.086, 1.0969, 1.1071, 1.117, 1.1267, 1.1365, 1.1467, 1.1576, 1.1698, 1.1843, 1.2033, 1.237, 10000],
		5: [-10000, 0.9886, 1.0181, 1.0341, 1.0457, 1.0552, 1.0632, 1.0704, 1.077, 1.0831, 1.0888, 1.0943, 1.0995, 1.1046, 1.1096, 1.1145, 1.1194, 1.1242, 1.1291, 1.134, 1.139, 1.1441, 1.1493, 1.1548, 1.1605, 1.1666, 1.1732, 1.1804, 1.1885, 1.1979, 1.2095, 1.2255, 1.255, 10000]
	},

	'e0111': {
		2: [-10000, 0.9096, 0.9663, 1.0097, 1.0663, 10000],
		3: [-10000, 0.8835, 0.9276, 0.9547, 0.9773, 0.9987, 1.0213, 1.0484, 1.0925, 10000],
		4: [-10000, 0.8611, 0.8982, 0.9192, 0.9351, 0.9485, 0.9606, 0.9718, 0.9826, 0.9933, 1.0041, 1.0154, 1.0274, 1.0409, 1.0568, 1.0778, 1.1149, 10000],
		5: [-10000, 0.8413, 0.8738, 0.8914, 0.9042, 0.9146, 0.9235, 0.9314, 0.9386, 0.9453, 0.9516, 0.9577, 0.9635, 0.9691, 0.9746, 0.98, 0.9853, 0.9906, 0.996, 1.0014, 1.0069, 1.0125, 1.0183, 1.0243, 1.0306, 1.0373, 1.0445, 1.0525, 1.0614, 1.0717, 1.0845, 1.1021, 1.1347, 10000]
	},

	'e0113': {
		2: [-10000, 0.9334, 0.9658, 0.9907, 1.0231, 10000],
		3: [-10000, 0.9184, 0.9436, 0.9592, 0.9721, 0.9844, 0.9973, 1.0129, 1.0381, 10000],
		4: [-10000, 0.9056, 0.9268, 0.9388, 0.948, 0.9557, 0.9626, 0.969, 0.9752, 0.9813, 0.9875, 0.994, 1.0009, 1.0086, 1.0177, 1.0297, 1.051, 10000]
	},

	'e0121': {
		2: [-10000, 0.7482, 0.7751, 0.7957, 0.8226, 10000],
		3: [-10000, 0.7358, 0.7567, 0.7696, 0.7803, 0.7905, 0.8012, 0.8141, 0.835, 10000],
		4: [-10000, 0.7252, 0.7428, 0.7528, 0.7603, 0.7667, 0.7724, 0.7777, 0.7829, 0.7879, 0.7931, 0.7984, 0.8041, 0.8105, 0.818, 0.828, 0.8456, 10000]
	},

	'e0123': {
		2: [-10000, 0.7432, 0.7714, 0.7929, 0.821, 10000],
		3: [-10000, 0.7302, 0.7521, 0.7656, 0.7768, 0.7874, 0.7987, 0.8121, 0.834, 10000],
		4: [-10000, 0.7191, 0.7376, 0.748, 0.7559, 0.7625, 0.7685, 0.7741, 0.7795, 0.7848, 0.7902, 0.7957, 0.8017, 0.8084, 0.8163, 0.8267, 0.8451, 10000]
	},

	'e0127': {
		2: [-10000, 0.761102322966032, 0.802752045694355, 0.834665190967747, 0.87631491369607, 10000],
		3: [-10000, 0.7419, 0.7743, 0.7942, 0.8108, 0.8266, 0.8432, 0.8631, 0.8955, 10000],
		4: [-10000, 0.7254, 0.7527, 0.7681, 0.7798, 0.7897, 0.7986, 0.8068, 0.8148, 0.8226, 0.8306, 0.8389, 0.8477, 0.8576, 0.8693, 0.8847, 0.912, 10000],
		5: [-10000, 0.710848584856612, 0.734782323437465, 0.747709286481988, 0.757120714388887, 0.764749637279928, 0.771296422687713, 0.777118944699481, 0.782426954186565, 0.787355322102825, 0.791996944616483, 0.796419422975603, 0.800674325030856, 0.80480265748718, 0.808838445683325, 0.812811030861894, 0.816746788988469, 0.820670447673633, 0.824606205800208, 0.828578790978777, 0.832614579174923, 0.836742911631246, 0.840997813686499, 0.845420292045619, 0.850061914559277, 0.854990282475537, 0.860298291962621, 0.866120813974389, 0.872667599382174, 0.880296522273215, 0.889707950180114, 0.902634913224637, 0.92656865180549, 10000]
	},

	'e0154': {
		2: [-10000, 0.956793251287651, 1.02514126603507, 1.07751136554388, 1.1458593802913, 10000],
		3: [-10000, 0.925255827173809, 0.97842268025498, 1.01115979502525, 1.03839888838614, 1.06425374319281, 1.0914928365537, 1.12422995132397, 1.17739680440514, 10000],
		4: [-10000, 0.898251315544251, 0.943015318882545, 0.968327649909676, 0.987521762069983, 1.00373456725904, 1.01827033098217, 1.03183361842079, 1.04488256415549, 1.05777006742346, 1.07081901315816, 1.08438230059678, 1.0989180643199, 1.11513086950897, 1.13432498166927, 1.1596373126964, 1.2044013160347, 10000],
		5: [-10000, 0.874325877958624, 0.913601614039277, 0.934815014816399, 0.950259353246385, 0.96277856586295, 0.973521969571006, 0.983076842791285, 0.991787390831928, 0.999874939582743, 1.00749193348416, 1.01474934259159, 1.02173168553457, 1.02850636034798, 1.03512916821024, 1.04164825867631, 1.04810691522554, 1.05454571635341, 1.06100437290264, 1.0675234633687, 1.07414627123097, 1.08092094604438, 1.08790328898735, 1.09516069809479, 1.10277769199621, 1.11086524074702, 1.11957578878766, 1.12913066200794, 1.139874065716, 1.15239327833256, 1.16783761676255, 1.18905101753967, 1.22832675362032, 10000]
	},

	'e0202': {
		2: [-10000, 0.529744730623774, 0.655279527028094, 0.751467687048153, 0.877002483452473, 10000],
		3: [-10000, 0.471819944809569, 0.569471502090752, 0.629599759691126, 0.679629801558416, 0.727117412517831, 0.777147454385121, 0.837275711985495, 0.934927269266678, 10000],
		4: [-10000, 0.422220759204841, 0.504438802651653, 0.550929960188287, 0.586183785351183, 0.615961844100615, 0.642659680845739, 0.667571370434572, 0.691538368627062, 0.715208845449186, 0.739175843641676, 0.764087533230508, 0.790785369975632, 0.820563428725065, 0.85581725388796, 0.902308411424595, 0.984526454871406, 10000],
		5: [-10000, 0.378276908793278, 0.450414651954833, 0.489377304433642, 0.517743920309192, 0.540737957703511, 0.560470366935338, 0.578019802260075, 0.594018465555602, 0.60887286607631, 0.622863132171858, 0.636192681592144, 0.649017150638415, 0.661460195642274, 0.673624306620123, 0.685597919861457, 0.697460534129781, 0.709286679946466, 0.72114929421479, 0.733122907456125, 0.745287018433974, 0.757730063437832, 0.770554532484103, 0.783884081904389, 0.797874347999938, 0.812728748520645, 0.828727411816172, 0.84627684714091, 0.866009256372736, 0.889003293767056, 0.917369909642605, 0.956332562121415, 1.02847030528297, 10000],
		6: [-10000, 0.338477525410902, 0.403400016530315, 0.437474529234453, 0.461724121435083, 0.480974633353786, 0.497164572397242, 0.511277848643227, 0.523886161759762, 0.535352763767027, 0.545924044811749, 0.555774101659778, 0.565032560438953, 0.573797684959345, 0.582146200018824, 0.590139313992355, 0.59782677189309, 0.605249667636653, 0.612442447452027, 0.619434370280568, 0.626250594291679, 0.63291300018817, 0.639440825626777, 0.645851161779212, 0.652159347808745, 0.658379288815535, 0.66452371583379, 0.670604401625723, 0.676632342617213, 0.682617914902886, 0.688571010514323, 0.694501158905878, 0.700417637728221, 0.706329576348026, 0.712246055170369, 0.718176203561924, 0.724129299173361, 0.730114871459034, 0.736142812450524, 0.742223498242457, 0.748367925260712, 0.754587866267502, 0.760896052297035, 0.767306388449471, 0.773834213888077, 0.780496619784569, 0.787312843795679, 0.794304766624221, 0.801497546439594, 0.808920442183158, 0.816607900083893, 0.824601014057424, 0.832949529116902, 0.841714653637295, 0.85097311241647, 0.860823169264499, 0.871394450309221, 0.882861052316485, 0.89546936543302, 0.909582641679005, 0.925772580722462, 0.945023092641164, 0.969272684841794, 1.00334719754593, 1.06826968866534, 10000]
	},

	'e0203': {
		2: [-10000, 0.64692568370861, 0.696017887693048, 0.733633663619607, 0.782725867604045, 10000],
		3: [-10000, 0.624273355568765, 0.662461414230896, 0.685975441992855, 0.705540415936197, 0.724111135376458, 0.7436761093198, 0.767190137081759, 0.805378195743891, 10000],
		4: [-10000, 0.604876874217284, 0.637029433308589, 0.655210475184457, 0.66899699514376, 0.680642137178167, 0.691082713695294, 0.700824791443266, 0.710197433914284, 0.719454117398371, 0.728826759869389, 0.738568837617362, 0.749009414134488, 0.760654556168895, 0.774441076128198, 0.792622118004066, 0.824774677095371, 10000],
		5: [-10000, 0.587691993768236, 0.615902505138491, 0.631139415854665, 0.642232592670969, 0.651224744700116, 0.658941389701038, 0.66580435107465, 0.672060860540314, 0.677869889441524, 0.68334093376867, 0.688553699780628, 0.693568894520132, 0.698434927851873, 0.703191879984536, 0.707874335212411, 0.712513382680816, 0.71713816863184, 0.721777216100244, 0.72645967132812, 0.731216623460782, 0.736082656792523, 0.741097851532027, 0.746310617543985, 0.751781661871131, 0.757590690772341, 0.763847200238005, 0.770710161611618, 0.778426806612539, 0.787418958641686, 0.79851213545799, 0.813749046174164, 0.84195955754442, 10000]
	},

	'e0207': {
		2: [-10000, 0.896040087780428, 0.991522491329828, 1.06468369423718, 1.16016609778658, 10000],
		3: [-10000, 0.851982201575487, 0.926256471869134, 0.971990329904064, 1.01004343377628, 1.04616275179073, 1.08421585566295, 1.12994971369788, 1.20422398399152, 10000],
		4: [-10000, 0.814256809162095, 0.876792270465501, 0.91215368095517, 0.93896791937606, 0.961617262059341, 0.981923772246168, 1.00087172983485, 1.01910115035447, 1.03710503521254, 1.05533445573216, 1.07428241332084, 1.09458892350767, 1.11723826619095, 1.14405250461184, 1.17941391510151, 1.24194937640491, 10000],
		5: [-10000, 0.780832893413019, 0.835701227135581, 0.865336418453091, 0.88691221052094, 0.904401592115744, 0.919410162769041, 0.93275835238444, 0.944927016920355, 0.95622534937974, 0.966866416805955, 0.97700493977546, 0.986759296049659, 0.996223539259702, 1.00547562383276, 1.01458281486082, 1.02360557950574, 1.03260060606127, 1.04162337070619, 1.05073056173424, 1.05998264630731, 1.06944688951735, 1.07920124579155, 1.08933976876105, 1.09998083618727, 1.11127916864665, 1.12344783318257, 1.13679602279797, 1.15180459345126, 1.16929397504607, 1.19086976711392, 1.22050495843143, 1.27537329215399, 10000],
		6: [-10000, 0.750561280333162, 0.79994165671559, 0.825858904099564, 0.844303267056199, 0.858945304166612, 0.871259454007646, 0.881994083580675, 0.891584030555939, 0.900305586264428, 0.908345897033827, 0.915838159549722, 0.922880190309396, 0.929546988526093, 0.935896911469195, 0.941976514542749, 0.947823634056052, 0.953469526248912, 0.958940391097675, 0.964258483103043, 0.969442937695407, 0.974510397448751, 0.97947549462268, 0.984351228848867, 0.989149267172836, 0.993880185884376, 0.998553668272723, 1.00317866876081, 1.00776355128595, 1.01231620795823, 1.01684416270723, 1.0213546636842, 1.02585476751744, 1.03035141804957, 1.03485152188281, 1.03936202285978, 1.04388997760878, 1.04844263428106, 1.0530275168062, 1.05765251729429, 1.06232599968263, 1.06705691839417, 1.07185495671814, 1.07673069094433, 1.08169578811826, 1.0867632478716, 1.09194770246397, 1.09726579446933, 1.1027366593181, 1.10838255151096, 1.11422967102426, 1.12030927409781, 1.12665919704092, 1.13332599525761, 1.14036802601729, 1.14786028853318, 1.15590059930258, 1.16462215501107, 1.17421210198633, 1.18494673155936, 1.1972608814004, 1.21190291851081, 1.23034728146744, 1.25626452885142, 1.30564490523385, 10000]
	},

	'e0210': {
		2: [-10000, 0.861223224447813, 0.971831067631968, 1.0565817919281, 1.16718963511226, 10000],
		3: [-10000, 0.810186095226704, 0.896226208754144, 0.949204801768103, 0.993285926555058, 1.03512693300501, 1.07920805779197, 1.13218665080593, 1.21822676433337, 10000],
		4: [-10000, 0.766484594919144, 0.838926345863251, 0.879889384083267, 0.910951286256757, 0.937188528414504, 0.960711808211294, 0.982661326067394, 1.00377848285454, 1.02463437670553, 1.04575153349268, 1.06770105134878, 1.09122433114557, 1.11746157330331, 1.1485234754768, 1.18948651369682, 1.26192826464093, 10000],
		5: [-10000, 0.727765971442306, 0.791326039339386, 0.8256557636819, 0.850649393260259, 0.870909280997761, 0.888295370659534, 0.903758057069701, 0.917854368942014, 0.930942478776454, 0.943269205726597, 0.955013779777212, 0.966313330991249, 0.977276812114091, 0.987994526389786, 0.998544394423642, 1.00899646202835, 1.01941639753172, 1.02986846513643, 1.04041833317028, 1.05113604744598, 1.06209952856882, 1.07339907978286, 1.08514365383347, 1.09747038078362, 1.11055849061806, 1.12465480249037, 1.14011748890054, 1.15750357856231, 1.17776346629981, 1.20275709587817, 1.23708682022068, 1.30064688811776, 10000],
		6: [-10000, 0.692699009281833, 0.749901768367369, 0.779924586474761, 0.801290734891768, 0.818252228155401, 0.832517071769836, 0.844952182118058, 0.856061279834014, 0.866164423766996, 0.875478706572393, 0.884157523716594, 0.892315087884454, 0.900037978637759, 0.907393797669681, 0.914436475256931, 0.921209841385533, 0.927750103623081, 0.934087612302672, 0.940248147277705, 0.946253875236942, 0.952124075115185, 0.957875697081338, 0.963523800047294, 0.969081899244581, 0.974562246360825, 0.979976058622915, 0.98533370893032, 0.990644886157562, 0.995918732610619, 1.00116396408996, 1.00638897693209, 1.0116019456111, 1.01681091394897, 1.02202388262798, 1.02724889547011, 1.03249412694945, 1.03776797340251, 1.04307915062975, 1.04843680093716, 1.05385061319925, 1.05933096031549, 1.06488905951278, 1.07053716247873, 1.07628878444489, 1.08215898432313, 1.08816471228237, 1.0943252472574, 1.10066275593699, 1.10720301817454, 1.11397638430314, 1.12101906189039, 1.12837488092231, 1.13609777167562, 1.14425533584348, 1.15293415298768, 1.16224843579307, 1.17235157972606, 1.18346067744201, 1.19589578779023, 1.21016063140467, 1.2271221246683, 1.24848827308531, 1.2785110911927, 1.33571385027824, 10000]
	},

	'e0404': {
		2: [-10000, 1.0127919645521, 1.05136978204073, 1.08092915034362, 1.11950696783225, 10000],
		3: [-10000, 0.994991228186773, 1.02500030982747, 1.04347819018056, 1.05885281043972, 1.07344612194462, 1.08882074220379, 1.10729862255687, 1.13730770419757, 10000],
		4: [-10000, 0.979749013398695, 1.00501525641928, 1.01930235006206, 1.03013612421854, 1.03928715284572, 1.0474916053384, 1.05514714616382, 1.06251240554901, 1.06978652683534, 1.07715178622053, 1.08480732704595, 1.09301177953863, 1.1021628081658, 1.11299658232228, 1.12728367596506, 1.15254991898565, 10000],
		5: [-10000, 0.96624472702012, 0.988413215504754, 1.00038674110115, 1.00910402237775, 1.01617026857699, 1.02223419112089, 1.02762726883616, 1.03254378226785, 1.03710865486567, 1.04140793117419, 1.04550422646282, 1.04944530515793, 1.05326914948636, 1.05700727522324, 1.06068685952634, 1.06433233298302, 1.06796659940133, 1.07161207285801, 1.07529165716111, 1.07902978289799, 1.08285362722641, 1.08679470592152, 1.09089100121015, 1.09519027751867, 1.0997551501165, 1.10467166354819, 1.11006474126345, 1.11612866380735, 1.12319491000659, 1.13191219128319, 1.14388571687959, 1.16605420536422, 10000]
	},

	'e0408': {
		2: [-10000, 0.780357438744899, 0.872880812332067, 0.943774726362923, 1.03629809995009, 10000],
		3: [-10000, 0.737664920403872, 0.809637407509811, 0.853953958782278, 0.890827784899249, 0.925827753795741, 0.962701579912712, 1.00701813118518, 1.07899061829112, 10000],
		4: [-10000, 0.701108649864294, 0.761706117393612, 0.795971666557852, 0.821954923227543, 0.843902355599215, 0.863579560596428, 0.881940314972215, 0.899604799968762, 0.917050738726228, 0.934715223722775, 0.953075978098562, 0.972753183095775, 0.994700615467447, 1.02068387213714, 1.05494942130138, 1.1155468888307, 10000],
		5: [-10000, 0.668720551862577, 0.721888498527962, 0.750605285866059, 0.771512437295953, 0.788459817409497, 0.803003267699192, 0.815937792685888, 0.82772934644932, 0.83867754000324, 0.848988837374938, 0.858813164304483, 0.868265229984025, 0.87743617329585, 0.886401532834747, 0.895226489124571, 0.903969635432311, 0.912685903262679, 0.921429049570419, 0.930254005860243, 0.93921936539914, 0.948390308710965, 0.957842374390506, 0.967666701320052, 0.977977998691749, 0.98892619224567, 1.0007177460091, 1.0136522709958, 1.02819572128549, 1.04514310139904, 1.06605025282893, 1.09476704016703, 1.14793498683241, 10000]
	},

	'e0411': {
		2: [-10000, 0.638536305041246, 0.738148211069767, 0.814473550588263, 0.914085456616783, 10000],
		3: [-10000, 0.592572966695749, 0.670059512466232, 0.717771306465868, 0.757470162654127, 0.795151599003903, 0.834850455192161, 0.882562249191798, 0.960048794962281, 10000],
		4: [-10000, 0.553215995105765, 0.618456042102971, 0.655346792308686, 0.683320715235783, 0.706949615547246, 0.728134358592096, 0.747901793226305, 0.766919614899607, 0.785702146758423, 0.804719968431724, 0.824487403065933, 0.845672146110784, 0.869301046422246, 0.897274969349343, 0.934165719555058, 0.999405766552265, 10000],
		5: [-10000, 0.518346534022531, 0.575587859126501, 0.606504737862056, 0.629013657747131, 0.64725943467708, 0.662917108488783, 0.676842591721233, 0.689537536791597, 0.701324508939214, 0.712425790107826, 0.723002792360722, 0.733179013154927, 0.743052573834157, 0.752704800263785, 0.762205866670756, 0.771618855352771, 0.781002906305258, 0.790415894987273, 0.799916961394245, 0.809569187823873, 0.819442748503103, 0.829618969297308, 0.840195971550204, 0.851297252718816, 0.863084224866433, 0.875779169936797, 0.889704653169246, 0.905362326980949, 0.923608103910899, 0.946117023795974, 0.977033902531529, 1.0342752276355, 10000],
		6: [-10000, 0.486765709019753, 0.538281729034146, 0.565319867102609, 0.584561927222798, 0.599837215343686, 0.612683937788718, 0.623882827558246, 0.633887528544057, 0.642986281354649, 0.651374326177877, 0.659190620303104, 0.666537210670148, 0.673492340126218, 0.680116889822968, 0.686459428631951, 0.692559429236906, 0.698449499675448, 0.704156973041948, 0.70970506631756, 0.715113742518344, 0.720400363989749, 0.725580195819671, 0.730666799858756, 0.735672347738558, 0.740607873161139, 0.745483478206733, 0.750308504566268, 0.755091677907789, 0.759841231666029, 0.764565015171538, 0.769270590049845, 0.773965318120076, 0.778656443537954, 0.783351171608185, 0.788056746486492, 0.792780529992001, 0.797530083750241, 0.802313257091761, 0.807138283451296, 0.81201388849689, 0.816949413919472, 0.821954961799274, 0.827041565838359, 0.832221397668281, 0.837508019139686, 0.84291669534047, 0.848464788616081, 0.854172261982582, 0.860062332421124, 0.866162333026079, 0.872504871835062, 0.879129421531812, 0.886084550987881, 0.893431141354925, 0.901247435480153, 0.90963548030338, 0.918734233113972, 0.928738934099784, 0.939937823869312, 0.952784546314344, 0.968059834435232, 0.987301894555421, 1.01434003262388, 1.06585605263828, 10000]
	},

	'e0413': {
		2: [-10000, 0.80103543798883, 0.888500279932582, 0.955518210052009, 1.04298305199576, 10000],
		3: [-10000, 0.760677048274695, 0.82871458262896, 0.870608214500441, 0.905466037428328, 0.938552452556262, 0.973410275484149, 1.01530390735563, 1.0833414417099, 10000],
		4: [-10000, 0.726119419203475, 0.783403840578679, 0.815795988915427, 0.840358662645194, 0.861106162752851, 0.879707555657677, 0.897064472263341, 0.913763186635261, 0.930255303349329, 0.94695401772125, 0.964310934326914, 0.98291232723174, 1.0036598273394, 1.02822250106916, 1.06061464940591, 1.11789907078112, 10000],
		5: [-10000, 0.695502076117573, 0.745763170921329, 0.772909924962568, 0.792674019422642, 0.808694835196243, 0.822443151233416, 0.834670506762265, 0.845817380748846, 0.856167003569943, 0.865914458124989, 0.875201752613804, 0.884137045380266, 0.892806585585363, 0.901281781901994, 0.909624251238518, 0.917889383391033, 0.926129106593558, 0.934394238746073, 0.942736708082596, 0.951211904399228, 0.959881444604324, 0.968816737370786, 0.978104031859601, 0.987851486414647, 0.998201109235744, 1.00934798322233, 1.02157533875117, 1.03532365478835, 1.05134447056195, 1.07110856502202, 1.09825531906326, 1.14851641386702, 10000]
	},

	'e0418': {
		2: [-10000, 0.617641055379049, 0.648684546902676, 0.672470910649697, 0.703514402173323, 10000],
		3: [-10000, 0.603316838913421, 0.627465086071182, 0.642334198931574, 0.654706124684683, 0.66644933286769, 0.678821258620799, 0.69369037148119, 0.717838618638951, 10000],
		4: [-10000, 0.591051459574215, 0.611383154109241, 0.6228799494002, 0.631597865500552, 0.638961679684809, 0.645563785972619, 0.651724184154599, 0.657650993450101, 0.663504464102271, 0.669431273397774, 0.675591671579754, 0.682193777867564, 0.68955759205182, 0.698275508152172, 0.709772303443131, 0.730103997978158, 10000],
		5: [-10000, 0.580184587702612, 0.598023525442586, 0.607658597217192, 0.614673375788045, 0.62035956977909, 0.625239195956664, 0.629578994660644, 0.633535303051779, 0.63720864677679, 0.640668265706243, 0.643964546220501, 0.647135924256211, 0.650212964035428, 0.653221026237504, 0.656181980266574, 0.659115485366692, 0.66203997218568, 0.664973477285798, 0.667934431314869, 0.670942493516945, 0.674019533296162, 0.677190911331872, 0.68048719184613, 0.683946810775583, 0.687620154500594, 0.691576462891728, 0.695916261595708, 0.700795887773282, 0.706482081764327, 0.713496860335181, 0.723131932109786, 0.74097086984976, 10000]
	},

	'e0601': {
		2: [-10000, 0.823794171416981, 1.00978957446757, 1.15230428834831, 1.33829969139891, 10000],
		3: [-10000, 0.737971402012795, 0.882654320816631, 0.971741807530547, 1.04586753257471, 1.11622633024118, 1.19035205528534, 1.27943954199926, 1.42412246080309, 10000],
		4: [-10000, 0.664484044070278, 0.786300293962704, 0.855182722037932, 0.907415645561862, 0.951535540585512, 0.991091703882231, 1.02800146817728, 1.06351155475127, 1.09858230806462, 1.13409239463861, 1.17100215893366, 1.21055832223037, 1.25467821725402, 1.30691114077795, 1.37579356885318, 1.49760981874561, 10000],
		5: [-10000, 0.599375768092555, 0.706256800279746, 0.763984812422665, 0.806013479406872, 0.840082003636209, 0.869318020369064, 0.895319689946217, 0.919023698023299, 0.941032734523496, 0.961760656592712, 0.981510040734185, 1.00051108552191, 1.018947003188, 1.03696964542752, 1.05471004159236, 1.07228597898395, 1.08980788383194, 1.10738382122352, 1.12512421738836, 1.14314685962789, 1.16158277729397, 1.1805838220817, 1.20033320622317, 1.22106112829239, 1.24307016479259, 1.26677417286967, 1.29277584244682, 1.32201185917968, 1.35608038340901, 1.39810905039322, 1.45583706253614, 1.56271809472333, 10000]
	},

	'e0604': {
		2: [-10000, 0.827949919777695, 0.879951402022736, 0.919796345725013, 0.971797827970054, 10000],
		3: [-10000, 0.803955180410594, 0.844406321189009, 0.869313825801045, 0.890038249692542, 0.909709498055207, 0.930433921946705, 0.955341426558741, 0.995792567337155, 10000],
		4: [-10000, 0.783409234237026, 0.817467202611556, 0.836725680527288, 0.851329210511569, 0.86366446127634, 0.874723762149365, 0.885043170159893, 0.894971249599774, 0.904776498147975, 0.914704577587857, 0.925023985598384, 0.936083286471409, 0.94841853723618, 0.963022067220461, 0.982280545136194, 1.01633851351072, 10000],
		5: [-10000, 0.765205951780333, 0.79508826072455, 0.811228133814032, 0.822978709066781, 0.832503749625897, 0.840677694681078, 0.847947365525998, 0.854574645205641, 0.860727925945761, 0.866523192634754, 0.872044875045227, 0.877357277810452, 0.882511679637314, 0.887550535948173, 0.892510480555131, 0.897424444993112, 0.902323302754637, 0.907237267192618, 0.912197211799576, 0.917236068110435, 0.922390469937297, 0.927702872702522, 0.933224555112995, 0.939019821801988, 0.945173102542109, 0.951800382221752, 0.959070053066672, 0.967243998121853, 0.976769038680969, 0.988519613933717, 1.0046594870232, 1.03454179596742, 10000]
	},

	'e0607': {
		2: [-10000, 0.775346595750878, 0.822396061155961, 0.858446635473251, 0.905496100878333, 10000],
		3: [-10000, 0.753636836508841, 0.7902358807375, 0.812771484070294, 0.83152235467672, 0.849320341952492, 0.868071212558918, 0.890606815891711, 0.92720586012037, 10000],
		4: [-10000, 0.735047447476233, 0.765862130742646, 0.78328665503308, 0.796499514534933, 0.807660099369526, 0.817666240951742, 0.827002948468871, 0.835985593001113, 0.844857103628099, 0.85383974816034, 0.86317645567747, 0.873182597259686, 0.884343182094279, 0.897556041596132, 0.914980565886565, 0.945795249152979, 10000],
		5: [-10000, 0.718577634093259, 0.745614299205902, 0.76021719835195, 0.770848785375766, 0.77946677176619, 0.786862325286852, 0.793439717164111, 0.7994358917452, 0.805003205537244, 0.810246598375772, 0.815242459922549, 0.820048971186034, 0.824712527684301, 0.82927154187871, 0.833759159002727, 0.838205174574703, 0.842637522054508, 0.847083537626485, 0.851571154750502, 0.856130168944911, 0.860793725443177, 0.865600236706663, 0.87059609825344, 0.875839491091967, 0.881406804884012, 0.8874029794651, 0.893980371342359, 0.901375924863021, 0.909993911253445, 0.920625498277261, 0.93522839742331, 0.962265062535952, 10000]
	}
})

fileList = tools.GetFileList('../data/rr')
for file in fileList:
	entroyRR = math.ceil(singleFile(file))
	identiter = re.search('(e\d+)_', file)[1]
	witnessGenerator = Witness(file, regionMap[identiter], 255)

	entroySum = 0
	for level in list(range(entroyRR))[2:]:
		quantizerList = witnessGenerator.quantizer(level)
		bitLists = [[] for x in list(range(level))]
		for quantizer in quantizerList:
			for pos in list(range(level)):
				bitLists[pos].append(quantizer[pos])
		entroyBit = list(map(calShannonEnt, bitLists))
		entroyQuantizer = sum(entroyBit)
		entroyWitness = 255 / level * entroyQuantizer
		entroySum += entroyWitness
		# print('%s when b=%d, quantizer的熵为: %s' %  (file, level, entroyBit))
		# print('%s when b=%d, witness的熵为: %f' %  (file, level, entroyWitness))
	# print('witness的平均熵为：%f' % (entroySum / (entroyRR - 2)))
	# print('%s witness的平均熵为：\n%f' % (file, entroySum / (entroyRR - 2)))

	# entroySum = 0
	# for level in list(range(entroyRR))[2:]:
	#     witnessList = witnessGenerator.getWitness(level)
	#     entroyWitness = calShannonEnt(witnessList)
	#     entroySum += entroyWitness
	#     print('%s when b=%d, witness的熵为: %f' %  (file, level, entroyWitness))
	# print('平均熵为：%f' % (entroySum / (entroyRR - 2)))

	# 计算IPI的熵，10-bit resolution
	ipis = list(map(lambda x: int(x), Witness.extractList(file)))
	ipis = list(filter(lambda x: x < 1024, ipis))
	ipiBins = list(map(tools.int2bin, ipis))
	bitLists = [[] for x in list(range(10))]
	for quantizer in ipiBins:
		for pos in list(range(10)):
			bitLists[pos].append(quantizer[pos])
	entroyBit = list(map(calShannonEnt, bitLists))
	entroyQuantizer = sum(entroyBit)
	# print('%s when b=%d, IPI的各bit位熵为: %s' % (file, level, entroyBit))
	print('%s IPI的熵为: \n%f' % (file, entroyQuantizer))
	# print('************')

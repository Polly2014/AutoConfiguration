# -*- coding: utf-8 -*-

class CConfigUiOne():
    def config2ui(self, ui, config):
        ui.cbox_cfg1_TM.setCurrentIndex(config.input_format_list.index(config.input_format))
        ui.list_cfg1_PM.clear()
        ui.list_cfg1_PM.addItems(config.datapath_list)
        ui.ledt_cfg1_PF.setText('{}'.format(config.PATH_FASTA))
        ui.ledt_cfg1_PRE.setText('{}'.format(config.PATH_RESULT_EXPORT))
        return ui
        
    def ui2config(self, ui, config):
        config.input_format = ui.cbox_cfg1_TM.currentText()
        item_num = ui.list_cfg1_PM.count()
        config.datapath_list =  [ui.list_cfg1_PM.item(i).text() for i in range(item_num)]
        config.PATH_FASTA = ui.ledt_cfg1_PF.text()
        config.PATH_RESULT_EXPORT = ui.ledt_cfg1_PRE.text()
        return config

class CConfigUiTwo():
    def config2ui(self, ui, config):
        # [group 1]
        ui.cbox_cfg2_NE.setCurrentIndex(config.NAME_ENZYME_LIST.index(config.NAME_ENZYME))
        ui.cbox_cfg2_NMMC.setCurrentIndex(int(config.NUMBER_MAX_MISS_CLV))
        ui.cbox_cfg2_TD.setCurrentIndex(config.TYPE_DIGEST_LIST.index(config.TYPE_DIGEST))
        ui.list_cfg2_NMF.clear()
        ui.list_cfg2_NMF.addItems(config.NAME_MOD_FIX)
        ui.list_cfg2_NMV.clear()
        ui.list_cfg2_NMV.addItems(config.NAME_MOD_VAR)
        ui.cbox_cfg2_NMM.setCurrentIndex(int(config.NUMBER_MAX_MOD)-1)
        
        # [group 2]
        ui.ledt_cfg2_US.setText(config.UAA_SEQ)
        ui.ledt_cfg2_UA.setText(config.UAA_AA)
        ui.ledt_cfg2_ULL.setText('{}'.format(config.UAA_LEN_LOW))
        ui.ledt_cfg2_ULU.setText('{}'.format(config.UAA_LEN_UP))
        ui.ledt_cfg2_UC.setText(config.UAA_COM)
        ui.ledt_cfg2_ULA.setText(config.UAA_LINKED_AA)
        
        # [group 3]
        ui.ledt_cfg2_PTP.setText(config.PPM_TOL_PRECURSOR)
        ui.ledt_cfg2_PTF.setText(config.PPM_TOL_FRAGMENT)
        ui.cbox_cfg2_TA.setCurrentIndex(config.TYPE_ACTIVATION_LIST.index(config.TYPE_ACTIVATION))
        ui.cbox_cfg2_NT.setCurrentIndex(int(config.NUMBER_THREAD)-1)
        ui.ledt_cfg2_FP.setText('{}'.format(config.FDR_PSM))
        
        return ui
    def ui2config(self, ui, config):
        # [group1]
        config.NAME_ENZYME = ui.cbox_cfg2_NE.currentText()
        config.NUMBER_MAX_MISS_CLV = ui.cbox_cfg2_NMMC.currentText()
        config.TYPE_DIGEST = ui.cbox_cfg2_TD.currentText()
        item_num = ui.list_cfg2_NMF.count()
        config.NAME_MOD_FIX  =  [ui.list_cfg2_NMF.item(i).text() for i in range(item_num)]
        item_num = ui.list_cfg2_NMV.count()
        config.NAME_MOD_VAR  =  [ui.list_cfg2_NMV.item(i).text() for i in range(item_num)]
        config.NUMBER_MAX_MOD = ui.cbox_cfg2_NMM.currentText()
        
        # [group 2]
        config.UAA_SEQ = ui.ledt_cfg2_US.text()
        config.UAA_AA = ui.ledt_cfg2_UA.text()
        config.UAA_LEN_LOW = ui.ledt_cfg2_ULL.text()
        config.UAA_LEN_UP = ui.ledt_cfg2_ULU.text()
        config.UAA_COM = ui.ledt_cfg2_UC.text()
        config.UAA_LINKED_AA = ui.ledt_cfg2_ULA.text()
        
        # [group 3]
        config.PPM_TOL_PRECURSOR = ui.ledt_cfg2_PTP.text()
        config.PPM_TOL_FRAGMENT = ui.ledt_cfg2_PTF.text()
        config.TYPE_ACTIVATION = ui.cbox_cfg2_TA.currentText()
        config.NUMBER_THREAD = ui.cbox_cfg2_NT.currentText()
        config.FDR_PSM = ui.ledt_cfg2_FP.text()
        return config
        
        
class CConfigUiThree():
    def update2ui(self, ui, config):
        ui.lbl_data_2.setText('HaHaHa')
        
    def ui2config(self, ui, config):
        pass

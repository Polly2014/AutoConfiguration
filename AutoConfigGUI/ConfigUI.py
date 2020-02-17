# -*- coding: utf-8 -*-

class ConfigUIOne():
    def update2ui(self, ui, config):
        # [data]
        ui.ledt_data_TM.setText(config.TYPE_MS2)
        ui.ledt_data_PM.setText(config.PATH_MS2)
        ui.ledt_data_PF.setText(config.PATH_FASTA)
        ui.ledt_data_PFE.setText(config.PATH_FASTA_EXPORT)
        ui.ledt_data_PRE.setText(config.PATH_RESULT_EXPORT)
        # [biology]
        ui.ledt_bio_NE.setText(config.NAME_ENZYME)
        ui.cbox_bio_TD.setCurrentIndex(int(config.TYPE_DIGEST))
        ui.ledt_bio_PT.setText(config.PATH_TEMP)
        # [mass]
        ui.list_mass_unselect.clear()
        ui.list_mass_selected.clear()
        ui.list_mass_unselect.addItems(config.LIST_UNSELECT)
        ui.list_mass_selected.addItems(config.LIST_SELECTED)
        return ui
    def update2config(self, ui, config):
        pass
        
class ConfigUITwo():
    def update2ui(self, ui, config):
        ui.lbl_data_2.setText('HaHaHa')
        
    def update2config(self, ui, config):
        pass

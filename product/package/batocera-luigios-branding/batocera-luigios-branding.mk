################################################################################
#
# batocera-luigios-branding
#
################################################################################

BATOCERA_LUIGIOS_BRANDING_VERSION = 0.1.0
BATOCERA_LUIGIOS_BRANDING_SITE = $(BR2_EXTERNAL_LUIGIOS_PATH)/branding
BATOCERA_LUIGIOS_BRANDING_SITE_METHOD = local
BATOCERA_LUIGIOS_BRANDING_LICENSE = CC-BY-SA-4.0
BATOCERA_LUIGIOS_BRANDING_LICENSE_FILES = LICENSES/CC-BY-SA-4.0.txt

define BATOCERA_LUIGIOS_BRANDING_INSTALL_TARGET_CMDS
	mkdir -p $(TARGET_DIR)/usr/share/luigios/branding
	cp -a $(@D)/assets $(TARGET_DIR)/usr/share/luigios/branding/
	$(INSTALL) -D -m 0644 $(@D)/brand-v1.json \
		$(TARGET_DIR)/usr/share/luigios/branding/brand-v1.json
	$(INSTALL) -D -m 0644 $(@D)/design-tokens-v1.json \
		$(TARGET_DIR)/usr/share/luigios/branding/design-tokens-v1.json
	$(INSTALL) -D -m 0644 $(@D)/PROVENANCE.json \
		$(TARGET_DIR)/usr/share/luigios/branding/PROVENANCE.json
endef

$(eval $(generic-package))

################################################################################
#
# batocera-deck-bua
#
################################################################################

BATOCERA_DECK_BUA_VERSION = 1.0.0
BATOCERA_DECK_BUA_SITE = $(BR2_EXTERNAL_LUIGIOS_PATH)/third_party/bua
BATOCERA_DECK_BUA_SITE_METHOD = local
BATOCERA_DECK_BUA_LICENSE = GPL-3.0
BATOCERA_DECK_BUA_LICENSE_FILES = LICENSE
BATOCERA_DECK_BUA_DEPENDENCIES = python3 python-pygame2

define BATOCERA_DECK_BUA_INSTALL_TARGET_CMDS
	$(INSTALL) -D -m 0755 $(@D)/bua_installerx86.py \
		$(TARGET_DIR)/usr/share/luigios/bua/bua_installerx86.py
	$(INSTALL) -D -m 0644 $(@D)/icon.png \
		$(TARGET_DIR)/usr/share/icons/hicolor/512x512/apps/bua.png
	$(INSTALL) -D -m 0644 $(@D)/LICENSE \
		$(TARGET_DIR)/usr/share/licenses/batocera-unofficial-addons/LICENSE
	$(INSTALL) -D -m 0755 $(BATOCERA_DECK_BUA_PKGDIR)/files/bua \
		$(TARGET_DIR)/usr/bin/bua
	$(INSTALL) -D -m 0644 $(BATOCERA_DECK_BUA_PKGDIR)/files/bua.desktop \
		$(TARGET_DIR)/usr/share/applications/bua.desktop
	$(INSTALL) -D -m 0755 $(BATOCERA_DECK_BUA_PKGDIR)/files/bua-port.sh \
		"$(TARGET_DIR)/usr/share/batocera/datainit/roms/ports/Batocera Unofficial Add-Ons.sh"
endef

$(eval $(generic-package))

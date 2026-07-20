################################################################################
#
# batocera-luigios-dev-connectivity
#
################################################################################

BATOCERA_LUIGIOS_DEV_CONNECTIVITY_VERSION = 0.1.0
BATOCERA_LUIGIOS_DEV_CONNECTIVITY_SITE = $(BATOCERA_LUIGIOS_DEV_CONNECTIVITY_PKGDIR)
BATOCERA_LUIGIOS_DEV_CONNECTIVITY_SITE_METHOD = local
BATOCERA_LUIGIOS_DEV_CONNECTIVITY_LICENSE = GPL-3.0-only
BATOCERA_LUIGIOS_DEV_CONNECTIVITY_LICENSE_FILES = LICENSE
BATOCERA_LUIGIOS_DEV_CONNECTIVITY_DEPENDENCIES = connman

define BATOCERA_LUIGIOS_DEV_CONNECTIVITY_INSTALL_TARGET_CMDS
	$(INSTALL) -D -m 0755 $(@D)/files/luigios-dev-connectivity-guard \
		$(TARGET_DIR)/usr/libexec/luigios/dev-connectivity-guard
	$(INSTALL) -D -m 0755 $(@D)/files/S07luigios-dev-connectivity \
		$(TARGET_DIR)/etc/init.d/S07luigios-dev-connectivity
	$(INSTALL) -D -m 0644 $(@D)/files/package-files.manifest \
		$(TARGET_DIR)/usr/share/luigios/manifests/dev-connectivity.files
endef

$(eval $(generic-package))

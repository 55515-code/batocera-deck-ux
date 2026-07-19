################################################################################
#
# batocera-deck-desktop-host
#
################################################################################

BATOCERA_DECK_DESKTOP_HOST_VERSION = 0.1.0
BATOCERA_DECK_DESKTOP_HOST_SITE = $(BATOCERA_DECK_DESKTOP_HOST_PKGDIR)
BATOCERA_DECK_DESKTOP_HOST_SITE_METHOD = local
BATOCERA_DECK_DESKTOP_HOST_LICENSE = GPL-3.0-only
BATOCERA_DECK_DESKTOP_HOST_LICENSE_FILES = LICENSE
BATOCERA_DECK_DESKTOP_HOST_DEPENDENCIES = acl dbus jq pipewire sdl2 util-linux

define BATOCERA_DECK_DESKTOP_HOST_BUILD_CMDS
	$(TARGET_CC) $(TARGET_CFLAGS) -Wall -Wextra -Werror \
		$(@D)/src/plasma-gamepad-bridge.c \
		-o $(@D)/plasma-gamepad-bridge \
		$(TARGET_LDFLAGS) -lSDL2 -lm
endef

define BATOCERA_DECK_DESKTOP_HOST_INSTALL_TARGET_CMDS
	$(INSTALL) -D -m 0755 $(@D)/plasma-gamepad-bridge \
		$(TARGET_DIR)/usr/libexec/batocera-deck-desktop/plasma-gamepad-bridge
	$(INSTALL) -D -m 0755 $(@D)/files/desktop \
		$(TARGET_DIR)/usr/bin/batocera-deck-desktop
	$(INSTALL) -D -m 0755 $(@D)/files/arch-plasma-session.sh \
		$(TARGET_DIR)/usr/libexec/batocera-deck-desktop/arch-plasma-session
	$(INSTALL) -D -m 0755 $(@D)/files/arch-plasma-mounts.sh \
		$(TARGET_DIR)/usr/libexec/batocera-deck-desktop/arch-plasma-mounts
	$(INSTALL) -D -m 0755 $(@D)/files/desktop-controller.sh \
		$(TARGET_DIR)/usr/libexec/batocera-deck-desktop/desktop-controller
	$(INSTALL) -D -m 0755 $(@D)/files/desktop-host-service \
		$(TARGET_DIR)/usr/share/batocera/services/deck_desktop_host
	$(INSTALL) -D -m 0755 $(@D)/files/S05deck-desktop-runtime \
		$(TARGET_DIR)/etc/init.d/S05deck-desktop-runtime
	$(INSTALL) -D -m 0644 $(@D)/files/90-deck-desktop-pulse.conf \
		$(TARGET_DIR)/usr/share/pipewire/pipewire-pulse.conf.d/90-deck-desktop-pulse.conf
	$(INSTALL) -D -m 0644 $(@D)/files/deck-desktop-connman.conf \
		$(TARGET_DIR)/etc/dbus-1/system.d/deck-desktop-connman.conf
	$(INSTALL) -D -m 0755 $(@D)/files/desktop-mode-port.sh \
		"$(TARGET_DIR)/usr/share/batocera/datainit/roms/ports/Desktop Mode.sh"
	$(INSTALL) -D -m 0644 $(@D)/files/package-files.manifest \
		$(TARGET_DIR)/usr/share/luigios/manifests/desktop-host.files
endef

$(eval $(generic-package))

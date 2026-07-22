################################################################################
#
# batocera-deck-desktop-host
#
################################################################################

BATOCERA_DECK_DESKTOP_HOST_VERSION = 0.2.0
BATOCERA_DECK_DESKTOP_HOST_SITE = $(BATOCERA_DECK_DESKTOP_HOST_PKGDIR)
BATOCERA_DECK_DESKTOP_HOST_SITE_METHOD = local
BATOCERA_DECK_DESKTOP_HOST_LICENSE = GPL-3.0-only
BATOCERA_DECK_DESKTOP_HOST_LICENSE_FILES = LICENSE
BATOCERA_DECK_DESKTOP_HOST_DEPENDENCIES = \
	acl \
	batocera-luigios-branding \
	batocera-onscreen-keyboard \
	dbus \
	jq \
	pipewire \
	sdl2 \
	util-linux \
	wlrctl

define BATOCERA_DECK_DESKTOP_HOST_BUILD_CMDS
	$(TARGET_CC) $(TARGET_CFLAGS) -Wall -Wextra -Werror \
		-fstack-protector-strong -fPIE \
		$(@D)/src/cosmic-gamepad-bridge.c \
		-o $(@D)/cosmic-gamepad-bridge \
		$(TARGET_LDFLAGS) -Wl,-z,relro -Wl,-z,now \
		-Wl,-z,noexecstack -pie -lSDL2 -lm
endef

define BATOCERA_DECK_DESKTOP_HOST_INSTALL_TARGET_CMDS
	$(INSTALL) -D -m 0755 $(@D)/cosmic-gamepad-bridge \
		$(TARGET_DIR)/usr/libexec/batocera-deck-desktop/cosmic-gamepad-bridge
	$(INSTALL) -D -m 0755 $(@D)/files/desktop \
		$(TARGET_DIR)/usr/bin/batocera-deck-desktop
	$(INSTALL) -D -m 0755 $(@D)/files/arch-cosmic-session.sh \
		$(TARGET_DIR)/usr/libexec/batocera-deck-desktop/arch-cosmic-session
	$(INSTALL) -D -m 0755 $(@D)/files/arch-cosmic-mounts.sh \
		$(TARGET_DIR)/usr/libexec/batocera-deck-desktop/arch-cosmic-mounts
	$(INSTALL) -D -m 0755 $(@D)/files/desktop-controller.sh \
		$(TARGET_DIR)/usr/libexec/batocera-deck-desktop/desktop-controller
	$(INSTALL) -D -m 0755 $(@D)/files/cosmic-brand-setup \
		$(TARGET_DIR)/usr/libexec/batocera-deck-desktop/cosmic-brand-setup
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

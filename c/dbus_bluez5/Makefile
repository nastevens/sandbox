APP_NAME = dbus_bluz5

SOURCES = main.c

override INCLUDES += -I$(BLUEZ_INCLUDE)

PKG_CONFIG ?= pkg-config

CFLAGS = -Wall -g -BLUEZ5

# DBus
LIBS += $(shell $(PKG_CONFIG) --libs --static dbus-1)
CFLAGS += $(shell $(PKG_CONFIG) --cflags dbus-1)

# BlueZ
LIBS += $(shell $(PKG_CONFIG) --libs bluez)
CFLAGS += $(shell $(PKG_CONFIG) --cflags bluez)

OBJECTS = $(SOURCES:.c=.o)

all: $(OBJECTS)
	$(CC) -o $(APP_NAME) $(OBJECTS) $(LDFLAGS) $(LIBS)

.c.o:
	$(CC) -c $(CFLAGS) $(INCLUDES) $< -o $@

clean:
	rm -f $(APP_NAME)

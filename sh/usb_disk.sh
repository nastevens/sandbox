#!/bin/bash
MNT=`/usr/bin/which mount`
UMNT=`/usr/bin/which umount`
RSYNC=`/usr/bin/which rsync`
USB_PATH='/mnt/usb'
BK_PATH='/home/common/backup/nicks_disk'
TR_PATH='/thinkingrock/program/bin/tr'

if grep -q $USB_PATH /etc/mtab; then
	if $RSYNC -rtv --delete-delay $BK_PATH/ $USB_PATH && $UMNT $USB_PATH; then
		kdialog --passivepopup "nicks_disk synced and successfully unmounted" 5 --title "Sync/Unmount Successful!" &
	else
		kdialog --error "nicks_disk sync failed - aborting" --title "Sync Failed!"
	fi
else
	if $MNT $USB_PATH && $RSYNC -rtv --delete-delay $USB_PATH/ $BK_PATH; then
		kdialog --passivepopup "nicks_disk synced successfully to $BK_PATH" 5 --title "Sync Successful!" &
		${BK_PATH}${TR_PATH}
	else
		kdialog --error "nicks_disk sync failed - aborting" --title "Sync Failed!"
	fi
fi

// December 12, 2004.  Lissa Avery, CSSE 332

struct bootSectorStruct
{
  int bytesPerSector;
  int sectorsPerCluster;
  int numberReservedSectors;
  int numberOfFATs;
  int maxNumberRootEntries;
  int totalSectorCount;
  int sectorsPerFAT;
  int sectorsPerTrack;
  int numberHeads;
  int sectorCountFAT32;
  int bootSig;
  int volumeID;
  char volumeLabel[12];
  char fileSysType[9];
};

typedef struct bootSectorStruct BootSector;

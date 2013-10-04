BEGIN;

CREATE TABLE IF NOT EXISTS "log_log" (
    "id" INTEGER NOT NULL PRIMARY KEY,
    "date" DATE NOT NULL,
    "new_rootnames" INTEGER NOT NULL,
    "total_rootnames" INTEGER NOT NULL,
    "missing_rootnames" INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS "missing" (
    "id" INTEGER NOT NULL PRIMARY KEY,
    "date" DATE NOT NULL UNIQUE,
    "flt" INTEGER NOT NULL,
    "asn" INTEGER NOT NULL,
    "drz" INTEGER NOT NULL,
    "ima" INTEGER NOT NULL,
    "jif" INTEGER NOT NULL,
    "jit" INTEGER NOT NULL,
    "jpg" INTEGER NOT NULL,
    "raw" INTEGER NOT NULL,
    "spt" INTEGER NOT NULL,
    "trl" INTEGER NOT NULL,
    "crj" INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS "wfc3a_disk_use" (
    "id" INTEGER NOT NULL PRIMARY KEY,
    "date" NOT NULL,
    "size" REAL NOT NULL,
    "used" REAL NOT NULL,
    "available" REAL NOT NULL
);


CREATE TABLE IF NOT EXISTS "wfc3b_disk_use" (
    "id" INTEGER NOT NULL PRIMARY KEY,
    "date" NOT NULL,
    "size" REAL NOT NULL,
    "used" REAL NOT NULL,
    "available" REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS "wfc3c_disk_use" (
    "id" INTEGER NOT NULL PRIMARY KEY,
    "date" NOT NULL,
    "size" REAL NOT NULL,
    "used" REAL NOT NULL,
    "available" REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS "wfc3d_disk_use" (
    "id" INTEGER NOT NULL PRIMARY KEY,
    "date" NOT NULL,
    "size" REAL NOT NULL,
    "used" REAL NOT NULL,
    "available" REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS "wfc3e_disk_use" (
    "id" INTEGER NOT NULL PRIMARY KEY,
    "date" NOT NULL,
    "size" REAL NOT NULL,
    "used" REAL NOT NULL,
    "available" REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS "wfc3f_disk_use" (
    "id" INTEGER NOT NULL PRIMARY KEY,
    "date" NOT NULL,
    "size" REAL NOT NULL,
    "used" REAL NOT NULL,
    "available" REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS "wfc3g_disk_use" (
    "id" INTEGER NOT NULL PRIMARY KEY,
    "date" NOT NULL,
    "size" REAL NOT NULL,
    "used" REAL NOT NULL,
    "available" REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS "wfc3h_disk_use" (
    "id" INTEGER NOT NULL PRIMARY KEY,
    "date" NOT NULL,
    "size" REAL NOT NULL,
    "used" REAL NOT NULL,
    "available" REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS "wfc3i_disk_use" (
    "id" INTEGER NOT NULL PRIMARY KEY,
    "date" NOT NULL,
    "size" REAL NOT NULL,
    "used" REAL NOT NULL,
    "available" REAL NOT NULL
);

COMMIT;
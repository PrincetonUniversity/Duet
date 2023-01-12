#ifndef PRGA_RXI_H
#define PRGA_RXI_H

#include "stdint.h"
#include "util.h"
#include "prga_mmr.h"

typedef uint32_t rx_regid_t;
typedef uint64_t rx_data_t;
typedef uint32_t yami_regid_t;
typedef uint64_t yami_creg_t;
typedef int yami_id_t;

// -- Register IDs --
const rx_regid_t    PRGA_RXI_REGID_STATUS           = 0x000ull,
                    PRGA_RXI_REGID_ERRCODE          = 0x008ull,
                    PRGA_RXI_REGID_CLKDIV           = 0x010ull,
                    PRGA_RXI_REGID_TIMEOUT          = 0x018ull,
                    PRGA_RXI_REGID_RST_APP          = 0x020ull,
                    PRGA_RXI_REGID_RST_PROG         = 0x028ull,
                    PRGA_RXI_REGID_ENABLE_YAMI      = 0x030ull,

                    PRGA_RXI_REGID_SCRATCHPAD       = 0x080ull,
                    PRGA_RXI_REGID_PROG             = 0x0C0ull,

                    PRGA_RXI_REGID_HSR_IQ           = 0x100ull,
                    PRGA_RXI_REGID_HSR_OQ           = 0x120ull,
                    PRGA_RXI_REGID_HSR_TQ           = 0x140ull,
                    PRGA_RXI_REGID_HSR_TQ_NB        = 0x160ull,
                    PRGA_RXI_REGID_HSR_PLAIN        = 0x180ull,
                    PRGA_RXI_REGID_SOFTREG          = 0x200ull;
                    
const yami_regid_t  PRGA_YAMI_CREG_STATUS           = 0x00ull,
                    PRGA_YAMI_CREG_FEATURES         = 0x08ull,
                    PRGA_YAMI_CREG_TIMEOUT          = 0x10ull,
                    PRGA_YAMI_CREG_ERRCODE          = 0x18ull;

// -- low-level API --
inline void rx_store_1B(rx_regid_t regid, uint8_t data) {
    volatile uint8_t * addr = (uint8_t *)(PRGA_RXI_BASE_ADDR + regid);
    *addr = data;
    FENCE
}

inline void rx_store_2B(rx_regid_t regid, uint16_t data) {
    volatile uint16_t * addr = (uint16_t *)(PRGA_RXI_BASE_ADDR + regid);
    *addr = data;
    FENCE
}

inline void rx_store_4B(rx_regid_t regid, uint32_t data) {
    volatile uint32_t * addr = (uint32_t *)(PRGA_RXI_BASE_ADDR + regid);
    *addr = data;
    FENCE
}

inline void rx_store_8B(rx_regid_t regid, uint64_t data) {
    volatile uint64_t * addr = (uint64_t *)(PRGA_RXI_BASE_ADDR + regid);
    *addr = data;
    FENCE
}

inline void rx_store(rx_regid_t regid, rx_data_t data) {
    rx_store_8B(regid, data);
}

inline uint8_t rx_load_1B(rx_regid_t regid) {
    volatile uint8_t * addr = (uint8_t *)(PRGA_RXI_BASE_ADDR + regid);
    return *addr;
}

inline uint16_t rx_load_2B(rx_regid_t regid) {
    volatile uint16_t * addr = (uint16_t *)(PRGA_RXI_BASE_ADDR + regid);
    return *addr;
}

inline uint32_t rx_load_4B(rx_regid_t regid) {
    volatile uint32_t * addr = (uint32_t *)(PRGA_RXI_BASE_ADDR + regid);
    return *addr;
}

inline uint64_t rx_load_8B(rx_regid_t regid) {
    volatile uint64_t * addr = (uint64_t *)(PRGA_RXI_BASE_ADDR + regid);
    return *addr;
}

inline rx_data_t rx_load(rx_regid_t regid) {
    return rx_load_8B(regid);
}

inline void yami_cstore(yami_id_t yami_id, yami_regid_t regid, yami_creg_t data) {
    volatile yami_creg_t * addr = (yami_creg_t *)(PRGA_YAMI_BASE_ADDR[yami_id] + regid);
    *addr = data;
}

inline yami_creg_t yami_cload(yami_id_t yami_id, yami_regid_t regid) {
    volatile yami_creg_t * addr = (yami_creg_t *)(PRGA_YAMI_BASE_ADDR[yami_id] + regid);
    return *addr;
}

// -- middle-level API --
// -- RXI status --
typedef uint8_t rx_status_t;
const rx_status_t   PRGA_RXI_STATUS_RESET       = 0,
                    PRGA_RXI_STATUS_STANDBY     = 1,
                    PRGA_RXI_STATUS_ERROR_PROG  = 2,
                    PRGA_RXI_STATUS_ERROR_APP   = 3,
                    PRGA_RXI_STATUS_PROGRAMMING = 4,
                    PRGA_RXI_STATUS_ACTIVE      = 5;

inline rx_status_t rx_get_status() {
    return rx_load_1B(PRGA_RXI_REGID_STATUS);
}

inline void rx_activate() {
    rx_store_1B(PRGA_RXI_REGID_STATUS, 1);
}

inline void rx_deactivate() {
    rx_store_1B(PRGA_RXI_REGID_STATUS, 0);
}

// -- RXI ERR code --
typedef uint32_t rx_errcode_t;
const rx_errcode_t  PRGA_RXI_ERRCODE_NONE               = 0x00000000,
                    PRGA_RXI_ERRCODE_NOTOKEN            = 0x00000001,
                    PRGA_RXI_ERRCODE_TIMEOUT_REQ        = 0x01000000,
                    PRGA_RXI_ERRCODE_TIMEOUT_RESP       = 0x01000001,
                    PRGA_RXI_ERRCODE_PARITY             = 0x01000002,
                    PRGA_RXI_ERRCODE_UNEXPECTED_RESP    = 0x01000003,
                    PRGA_RXI_ERRCODE_YAMI               = 0x08000000;

inline rx_errcode_t rx_get_errcode() {
    return rx_load_4B(PRGA_RXI_REGID_ERRCODE);
}

// -- RXI clock divider --
typedef uint32_t rx_clkdiv_t;
inline void rx_set_clkdiv(rx_clkdiv_t div) {
    rx_store_4B(PRGA_RXI_REGID_CLKDIV, div);
}

inline rx_clkdiv_t rx_get_clkdiv() {
    return rx_load_4B(PRGA_RXI_REGID_CLKDIV);
}

// -- RXI timeout --
inline void rx_set_timeout(rx_data_t timeout) {
    rx_store(PRGA_RXI_REGID_TIMEOUT, timeout);
}

inline rx_data_t rx_get_timeout() {
    return rx_load(PRGA_RXI_REGID_TIMEOUT);
}

// -- RXI reset programming backend --
inline void rx_reset_prog(rx_data_t hold) {
    rx_store(PRGA_RXI_REGID_RST_PROG, hold);
}

// -- RXI reset application --
inline void rx_reset_app(rx_data_t hold) {
    rx_store(PRGA_RXI_REGID_RST_APP, hold);
}

// -- RXI enable YAMI --
inline void rx_set_enable_yami(rx_data_t bits) {
    rx_store(PRGA_RXI_REGID_ENABLE_YAMI, bits);
}

inline rx_data_t rx_get_enable_yami() {
    return rx_load(PRGA_RXI_REGID_ENABLE_YAMI);
}

// -- RXI Soft Registers --
inline void rx_set_softreg_1B(rx_regid_t regid, uint8_t data) {
    rx_store_1B(PRGA_RXI_REGID_SOFTREG + regid, data);
}

inline void rx_set_softreg_2B(rx_regid_t regid, uint16_t data) {
    rx_store_2B(PRGA_RXI_REGID_SOFTREG + regid, data);
}

inline void rx_set_softreg_4B(rx_regid_t regid, uint32_t data) {
    rx_store_4B(PRGA_RXI_REGID_SOFTREG + regid, data);
}

inline void rx_set_softreg_8B(rx_regid_t regid, uint64_t data) {
    rx_store_8B(PRGA_RXI_REGID_SOFTREG + regid, data);
}

inline void rx_set_softreg(rx_regid_t regid, rx_data_t data) {
    rx_store(PRGA_RXI_REGID_SOFTREG + regid, data);
}

inline uint8_t rx_get_softreg_1B(rx_regid_t regid) {
    return rx_load_1B(PRGA_RXI_REGID_SOFTREG + regid);
}

inline uint16_t rx_get_softreg_2B(rx_regid_t regid) {
    return rx_load_2B(PRGA_RXI_REGID_SOFTREG + regid);
}

inline uint32_t rx_get_softreg_4B(rx_regid_t regid) {
    return rx_load_4B(PRGA_RXI_REGID_SOFTREG + regid);
}

inline uint64_t rx_get_softreg_8B(rx_regid_t regid) {
    return rx_load_8B(PRGA_RXI_REGID_SOFTREG + regid);
}

inline rx_data_t rx_get_softreg(rx_regid_t regid) {
    return rx_load(PRGA_RXI_REGID_SOFTREG + regid);
}

// -- YAMI status --
const yami_creg_t   PRGA_YAMI_STATUS_RESET      = 0,
                    PRGA_YAMI_STATUS_INACTIVE   = 1,
                    PRGA_YAMI_STATUS_ACTIVE     = 2,
                    PRGA_YAMI_STATUS_ERROR      = 3;

inline yami_creg_t yami_get_status(yami_id_t yami_id) {
    return yami_cload(yami_id, PRGA_YAMI_CREG_STATUS);
}

inline void yami_activate(yami_id_t yami_id) {
    yami_cstore(yami_id, PRGA_YAMI_CREG_STATUS, 1);
}

inline void yami_deactivate(yami_id_t yami_id) {
    yami_cstore(yami_id, PRGA_YAMI_CREG_STATUS, 0);
}

// -- YAMI features --
const yami_creg_t   PRGA_YAMI_FEATURE_LOAD      = 1 << 0,
                    PRGA_YAMI_FEATURE_STORE     = 1 << 1,
                    PRGA_YAMI_FEATURE_SUBWORD   = 1 << 2,
                    PRGA_YAMI_FEATURE_NC        = 1 << 3,
                    PRGA_YAMI_FEATURE_AMO       = 1 << 4,
                    PRGA_YAMI_FEATURE_L1CACHE   = 1 << 5;

inline yami_creg_t yami_get_features(yami_id_t yami_id) {
    return yami_cload(yami_id, PRGA_YAMI_CREG_FEATURES);
}

inline void yami_set_features(yami_id_t yami_id, yami_creg_t features) {
    yami_cstore(yami_id, PRGA_YAMI_CREG_FEATURES, features);
}

// -- YAMI timeout --
inline yami_creg_t yami_get_timeout(yami_id_t yami_id) {
    return yami_cload(yami_id, PRGA_YAMI_CREG_TIMEOUT);
}

inline void yami_set_timeout(yami_id_t yami_id, yami_creg_t timeout) {
    yami_cstore(yami_id, PRGA_YAMI_CREG_TIMEOUT, timeout);
}

// -- YAMI ERR code --
const yami_creg_t   PRGA_YAMI_ERRCODE_NONE              = 0x00000000,
                    PRGA_YAMI_ERRCODE_TIMEOUT           = 0x01000000,
                    PRGA_YAMI_ERRCODE_PARITY            = 0x01000001,
                    PRGA_YAMI_ERRCODE_SIZE_OUT_OF_RANGE = 0x01000002,
                    PRGA_YAMI_ERRCODE_MISSING_FEATURES  = 0x80000000,
                    PRGA_YAMI_ERRCODE_INVAL_REQTYPE     = 0x81000000;

inline yami_creg_t yami_get_errcode(yami_id_t yami_id) {
    return yami_cload(yami_id, PRGA_YAMI_CREG_ERRCODE);
}

// -- Performance Marker --
int pause_perf_marker = 0;
#define perf_marker( x ) \
    if (!pause_perf_marker) \
    asm (   "addi zero,zero," #x ";\n"  \
            "addi zero,zero," #x ";\n"  \
        );

#endif /* #ifndef PRGA_RXI_H */

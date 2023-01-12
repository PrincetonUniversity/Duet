#include "stdint.h"
#include "stdio.h"
// #include "stdlib.h"
#include "prga_rxi.h"

#define     N 64    // Nx 8B numbers
#define     M 8     // number of tests

#ifndef VERSAL
const rx_regid_t    PRGA_POPCOUNT_SOFTREG_ADDR_LEN      = 0x400ull,     // additional effect: start popcount
                    PRGA_POPCOUNT_SOFTREG_ADDR_COUNT    = 0x500ull,
                    PRGA_POPCOUNT_SOFTREG_ADDR_ADDR     = 0x200ull;
#else /* #ifndef VERSAL */
const rx_regid_t    PRGA_POPCOUNT_SOFTREG_ADDR_LEN      = NA,     // additional effect: start popcount
                    PRGA_POPCOUNT_SOFTREG_ADDR_COUNT    = NA,
                    PRGA_POPCOUNT_SOFTREG_ADDR_ADDR     = NA;
#endif /* #ifndef VERSAL */

void init ()
{
    // configrue RXI/YAMI
    rx_set_clkdiv( 52 );    // 5.3ns
    rx_activate();
    rx_set_enable_yami( 1 );
    rx_reset_app( 100 );
    rx_set_timeout( 50000 );

    // make sure app is up
    rx_status_t status;
    while ((status = rx_get_status()) != PRGA_RXI_STATUS_ACTIVE) {
        if (status == PRGA_RXI_STATUS_ERROR_APP ||
                status == PRGA_RXI_STATUS_ERROR_PROG) {
            printf("E|RX errcode: 0x%08x\n", rx_get_errcode());
            exit (1);
        }
    }

    printf ("I|acc init\n");
}

uint64_t popcount_acc (
        uint64_t *  array,
        uint32_t    len
        )
{
    perf_marker (1024);
    rx_store    (PRGA_POPCOUNT_SOFTREG_ADDR_ADDR, array);
    rx_store    (PRGA_POPCOUNT_SOFTREG_ADDR_LEN,  len);

    uint64_t ret = rx_load(PRGA_POPCOUNT_SOFTREG_ADDR_COUNT);
    perf_marker (1025);
    return ret;
}

uint64_t popcount_ref (
        uint64_t *  array,
        uint32_t    len
        )
{
    const uint8_t lookup [256] = {
        0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4,
        1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
        1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
        1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
        3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
        1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
        3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
        3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
        3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
        4, 5, 5, 6, 5, 6, 6, 7, 5, 6, 6, 7, 6, 7, 7, 8
    };

    perf_marker (1028);
    uint8_t * array_u8 = (uint8_t *) array;

    uint64_t count = 0, len_u8 = len << 3;
    for (uint32_t i = 0; i < len_u8; i++) {
        count += lookup[array_u8[i]];
    }
    perf_marker (1029);

    return count;
}

int main (int argc, char ** argv) {
    uint64_t    data[N] = {};
    uint32_t    lfsr = 0xdeadbeef;

    init();

    for (int i = 0; i < M; i++) {

        // initialize arr
        for (int i = 0; i < N; i++) {
            lfsr ^= lfsr << 13;
            lfsr ^= lfsr >> 17;
            lfsr ^= lfsr << 5;

            uint64_t v = lfsr;

            lfsr ^= lfsr << 13;
            lfsr ^= lfsr >> 17;
            lfsr ^= lfsr << 5;

            data[i] = (v << 32) + lfsr;
        }

        printf ("I|call ref\n");
        uint64_t ref = popcount_ref (data, N);

        printf ("I|call acc\n");
        uint64_t acc = popcount_acc (data, N);

        if (ref == acc) {
            printf ("I|match\n");
        } else {
            printf ("E|ref (0x%016llx) != acc (0x%016llx)\n", ref, acc);
        }
    }

    return 0;
}

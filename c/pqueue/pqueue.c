/* Adapted from http://rosettacode.org/wiki/Priority_queue#C */

#include <stdio.h>
#include <stdlib.h>

#include "pqueue.h"

struct pqueue * pqueue_new ( int size )
{
    if (size < 4)
    {
        size = 4;
    }

    struct pqueue * q = malloc(sizeof *q);
    q->buf = malloc(sizeof(struct q_elem) * size);
    q->alloc = size;
    q->n = 1;

    return q;
}

void pqueue_free ( struct pqueue * q )
{
    free(q->buf);
    free(q);
}

void pqueue_push (
        struct pqueue * q,
        void * data,
        int priority )
{
    struct q_elem * b;
    int n, m;

    if (q->n >= q->alloc) {
        q->alloc *= 2;
        b = q->buf = realloc(q->buf, sizeof(struct q_elem) * q->alloc);
    }
    else
    {
        b = q->buf;
    }

    n = q->n++;
    /* append at end, the up heap */
    while ((m = n / 2) && (priority < b[m].priority))
    {
        b[n] = b[m];
        n = m;
    }
    b[n].data = data;
    b[n].priority = priority;
}

void * pqueue_pop (
        struct pqueue * q,
        int * priority )
{
    void * out;
    if (q->n == 1) return 0;

    struct q_elem * b = q->buf;

    out = b[1].data;
    if (priority)
    {
        *priority = b[1].priority;
    }

    /* pull last item to top, then down heap */
    --q->n;

    int n = 1, m;
    while ((m = n * 2) < q->n)
    {
        if (m + 1 < q->n && b[m].priority > b[m + 1].priority)
        {
            m++;
        }

        if (b[q->n].priority <= b[m].priority)
        {
            break;
        }

        b[n] = b[m];
        n = m;
    }

    b[n] = b[q->n];
    if (q->n < q->alloc / 2 && q->n >= 16)
    {
        q->buf = realloc(q->buf, (q->alloc /= 2) * sizeof(b[0]));
    }

    return out;
}

void * pqueue_peek (
        struct pqueue * q,
        int * priority )
{
    if (q->n == 1)
    {
        return 0;
    }

    if (priority)
    {
        *priority = q->buf[1].priority;
    }

    return q->buf[1].data;
}

#ifndef __PQUEUE_H__
#define __PQUEUE_H__


struct q_elem
{
    int priority;
    void * data;
};

struct pqueue
{
    int n;
    int alloc;
    struct q_elem * buf;
};

struct pqueue * pqueue_new ( int size );

void pqueue_free ( struct pqueue * q );

static inline void pqueue_purge ( struct pqueue * q )
{
    q->n = 1;
}

static inline int pqueue_size ( struct pqueue * q )
{
    return q->n - 1;
}

void pqueue_push (
        struct pqueue * q,
        void * data,
        int priority );

void * pqueue_pop (
        struct pqueue * q,
        int * priority );

void * pqueue_peek (
        struct pqueue * q,
        int * priority );

#endif /* end of include guard: __PQUEUE_H__ */

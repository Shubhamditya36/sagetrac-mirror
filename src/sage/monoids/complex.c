#include "complex.h"

Complexe prod (Complexe a, Complexe b)
{
	Complexe r;
	r.x = a.x*b.x - a.y*b.y;
	r.y = a.x*b.y + a.y*b.x;
	return r;
}

Complexe mul_i (Complexe a, int i)
{
	Complexe r;
	r.x = a.x*i;
	r.y = a.y*i;
	return r;
}

Complexe zero ()
{
	Complexe r;
	r.x = 0;
	r.y = 0;
	return r;
}

Complexe un ()
{
	Complexe r;
	r.x = 1;
	r.y = 0;
	return r;
}

Complexe add (Complexe a, Complexe b)
{
	Complexe r;
	r.x = a.x + b.x;
	r.y = a.y + b.y;
	return r;
}

void addOP (Complexe *a, Complexe b)
{
	double r = a->x + b.x;
	a->y = a->y + b.y;
	a->x = r;
}

double carre (double x)
{
	return x*x;
}

double cnorm (Complexe c)
{
	return carre(c.x) + carre(c.y);
}

Complexe inv (Complexe c)
{
	Complexe r;
	double cn = cnorm(c);
	r.x = c.x/cn;
	r.y = -c.y/cn;
	return r;
}

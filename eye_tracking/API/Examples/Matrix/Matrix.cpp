// Copyright (C) Smart Eye AB 2002-2023
// THE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
// ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
// THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
// PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
// OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
// OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
// TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
// WITH THE CODE OR THE USE OR OTHER DEALINGS IN THE CODE.
//----------------------------------------------------------------------------//
// Smart Eye AB
// F�rsta l�nggatan 28 B,
// 413 27 G�teborg, Sweden
// Contact: support@smarteye.se
//
// You are free to modify and use this code together with
// your purchased Smart Eye system.
//
// You MAY NOT distribute this code (modified or unmodified)
// without prior written consent from Smart Eye AB.
//----------------------------------------------------------------------------//

// Example code
// method for conversion of rodrigues form rotations to rotation matrices
// function for finding an intersection between a vector and a plane

#include "Matrix.h"
#include <cmath>

CPoint3D::CPoint3D()
{
}
CPoint3D::CPoint3D(double x, double y, double z)
{
  m_xyz[0] = x;
  m_xyz[1] = y;
  m_xyz[2] = z;
}

CVect3D::CVect3D()
{
}
CVect3D::CVect3D(double x, double y, double z)
{
  m_xyz[0] = x;
  m_xyz[1] = y;
  m_xyz[2] = z;
}

bool CVect3D::normalize()
{
  double len = length();
  if (len == 0.0)
    return false;
  m_xyz[0] /= len;
  m_xyz[1] /= len;
  m_xyz[2] /= len;
  return true;
}

double CVect3D::length() const
{
  return sqrt(sqrLength());
}

double CVect3D::sqrLength() const
{
  return m_xyz[0] * m_xyz[0] + m_xyz[1] * m_xyz[1] + m_xyz[2] * m_xyz[2];
}

CVect3D& CVect3D::operator+=(const CVect3D& rhs)
{
  m_xyz[0] += rhs.m_xyz[0];
  m_xyz[1] += rhs.m_xyz[1];
  m_xyz[2] += rhs.m_xyz[2];
  return *this;
}

CVect3D& CVect3D::operator-=(const CVect3D& rhs)
{
  m_xyz[0] -= rhs.m_xyz[0];
  m_xyz[1] -= rhs.m_xyz[1];
  m_xyz[2] -= rhs.m_xyz[2];
  return *this;
}

CVect3D& CVect3D::operator*=(const double& rhs)
{
  m_xyz[0] *= rhs;
  m_xyz[1] *= rhs;
  m_xyz[2] *= rhs;

  return *this;
}

CVect3D& CVect3D::operator/=(const double& rhs)
{
  m_xyz[0] /= rhs;
  m_xyz[1] /= rhs;
  m_xyz[2] /= rhs;

  return *this;
}

CMatrix::CMatrix()
{
}

void CMatrix::set2Unit()
{
  m_cols[0] = CVect3D(1.0, 0.0, 0.0);
  m_cols[1] = CVect3D(0.0, 1.0, 0.0);
  m_cols[2] = CVect3D(0.0, 0.0, 1.0);
}

void CMatrix::rodriguesToMatrix(const CVect3D& rod)
{
  // Uses Rodrigues formula:
  // R  = c*I + (1-c)*r*r^t + s*r^^
  // where:
  // R = rotation matrix.
  // r = rod.normalize() or 0,0,0
  // s = sin(rod.length());
  // c = cos(rod.length());
  //       |   0  -r.z   r.y |
  // r^^ = |  r.z   0   -r.x |
  //       | -r.y  r.x    0  |
  // I = unity matrix
  // r^t = r transposed

  double angle = rod.length();
  if (angle < 1e-10)
  {
    set2Unit();
    return;
  }

  // direction
  CVect3D r(rod);
  r /= angle;

  double c = cos(angle);
  double c1 = 1.0 - c;

  CVect3D sr(r);
  sr *= sin(angle);

  set(c + c1 * r.x() * r.x(),
      -sr.z() + c1 * r.y() * r.x(),
      sr.y() + c1 * r.z() * r.x(),
      sr.z() + c1 * r.x() * r.y(),
      c + c1 * r.y() * r.y(),
      -sr.x() + c1 * r.z() * r.y(),
      -sr.y() + c1 * r.x() * r.z(),
      sr.x() + c1 * r.y() * r.z(),
      c + c1 * r.z() * r.z());
}

void CMatrix::set(double m11,
                  double m12,
                  double m13,
                  double m21,
                  double m22,
                  double m23,
                  double m31,
                  double m32,
                  double m33)
{
  m_cols[0].m_xyz[0] = m11;
  m_cols[1].m_xyz[0] = m12;
  m_cols[2].m_xyz[0] = m13;
  m_cols[0].m_xyz[1] = m21;
  m_cols[1].m_xyz[1] = m22;
  m_cols[2].m_xyz[1] = m23;
  m_cols[0].m_xyz[2] = m31;
  m_cols[1].m_xyz[2] = m32;
  m_cols[2].m_xyz[2] = m33;
}

double operator*(const CVect3D& lhs, const CVect3D& rhs)
{
  return lhs.x() * rhs.x() + lhs.y() * rhs.y() + lhs.z() * rhs.z();
}

CVect3D operator*(double lhs, const CVect3D& rhs)
{
  CVect3D ret;

  ret.x() = lhs * rhs.x();
  ret.y() = lhs * rhs.y();
  ret.z() = lhs * rhs.z();

  return ret;
}

CVect3D operator+(const CVect3D& lhs, const CVect3D& rhs)
{
  CVect3D ret(lhs);

  ret.x() += rhs.x();
  ret.y() += rhs.y();
  ret.z() += rhs.z();

  return ret;
}

CVect3D operator-(const CVect3D& lhs, const CVect3D& rhs)
{
  CVect3D ret(lhs);

  ret.x() -= rhs.x();
  ret.y() -= rhs.y();
  ret.z() -= rhs.z();
  return ret;
}

bool findIntersectionBetweenLineAndPlane(const CVect3D& vectorParallelToLine,
                                         const CPoint3D& pointOnLine,
                                         const CVect3D& normalVectorToPlane,
                                         const CPoint3D& pointInPlane,
                                         CPoint3D& pointOfIntersection)
{
  // Calculate intersection between measured gaze and the gaze projection plane
  // The plane equation: nr + d = 0, , n is normalized and equal to the zAxis
  // The line equation: r = r0 + kt, k is normalized
  // Now simply find the t, ti, for wich the line intersects with the plane.
  // ti = -(d + nr0) / nk => ri = r0 + k (d + nr0) / nk

  CVect3D n = normalVectorToPlane;
  n.normalize();
  CVect3D k = vectorParallelToLine;
  k.normalize();

  // First calulate d
  double d = -(n.x() * pointInPlane.x() + n.y() * pointInPlane.y() + n.z() * pointInPlane.z());
  // Second, calculate ti

  CVect3D r0(pointOnLine.x(), pointOnLine.y(), pointOnLine.z());

  // calculate n * k

  double nk = n * k;

  if (nk == 0.0) // No intersection
    return false;

  double ti = (d + n * r0) / (n * k);
  ti *= -1.0;
  // Finally, calulate ri, the point of intersection
  CVect3D ri = r0 + ti * k;
  pointOfIntersection.x() = ri.x();
  pointOfIntersection.y() = ri.y();
  pointOfIntersection.z() = ri.z();

  return true;
}
// Copyright (C) Smart Eye AB 2002-2018
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
// Första långgatan 28 B,
// 413 27 Göteborg, Sweden
// Contact: support@smarteye.se
//
// You are free to modify and use this code together with
// your purchased Smart Eye system.
//
// You MAY NOT distribute this code (modified or unmodified)
// without prior written consent from Smart Eye AB.
//----------------------------------------------------------------------------//

#ifndef MATRIX_H
#define MATRIX_H

// Methods used to convert rodrigues form rotations to rotation matrices

class CPoint3D
{
private:
public:
  CPoint3D();
  CPoint3D(double x, double y, double z);

  double m_xyz[3];

  // access operators:
  double& x()
  {
    return m_xyz[0];
  }
  double& y()
  {
    return m_xyz[1];
  }
  double& z()
  {
    return m_xyz[2];
  }
  double x() const
  {
    return m_xyz[0];
  }
  double y() const
  {
    return m_xyz[1];
  }
  double z() const
  {
    return m_xyz[2];
  }
};

class CVect3D
{
public:
  CVect3D();
  double m_xyz[3];
  CVect3D(double x, double y, double z);

  bool normalize();
  double length() const; ///< returns length of vector
  double sqrLength() const;
  double& x()
  {
    return m_xyz[0];
  }
  double& y()
  {
    return m_xyz[1];
  }
  double& z()
  {
    return m_xyz[2];
  }
  double x() const
  {
    return m_xyz[0];
  }
  double y() const
  {
    return m_xyz[1];
  }
  double z() const
  {
    return m_xyz[2];
  }
  CVect3D operator-() const;
  CVect3D& operator+=(const CVect3D& rhs);
  CVect3D& operator-=(const CVect3D& rhs);
  CVect3D& operator*=(const double& rhs);
  CVect3D& operator/=(const double& rhs);
};

// operators

CVect3D operator+(const CVect3D& lhs, const CVect3D& rhs);
CVect3D operator-(const CVect3D& lhs, const CVect3D& rhs);
CVect3D operator*(double lhs, const CVect3D& rhs);
double operator*(const CVect3D& lhs, const CVect3D& rhs);
CVect3D operator/(const CVect3D& lhs, double rhs);
CVect3D cross(const CVect3D& lhs, const CVect3D& rhs);

class CMatrix
{
public:
  CMatrix();
  CVect3D m_cols[3]; // base vectors (columns)
  void set2Unit();
  void rodriguesToMatrix(const CVect3D& rod);
  void set(double m11,
           double m12,
           double m13,
           double m21,
           double m22,
           double m23,
           double m31,
           double m32,
           double m33);
};

bool findIntersectionBetweenLineAndPlane(const CVect3D& vectorParallelToLine,
                                         const CPoint3D& pointOnLine,
                                         const CVect3D& normalVectorToPlane,
                                         const CPoint3D& pointInPlane,
                                         CPoint3D& pointOfIntersection);

#endif //MATRIX_H

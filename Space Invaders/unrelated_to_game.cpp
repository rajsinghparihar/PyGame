#include<iostream>
using namespace std;

int main(void)
{
  int n,m;
  cin>>n>m;
  int ans = max(n,m);
  
  cout<<ans<<" "<<n<<" "<<" "<<m<<" "<<m/ans<<" "<<n/ans<<" ";
return 0;
}

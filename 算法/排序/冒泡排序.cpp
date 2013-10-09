#include<iostream>
using namespace std;

#define N 10

int main()
{
   int tosort[N] = {5,4,6,1,2,3,9,7,8,10};
   int i,j,temp;
   
   //冒泡排序
   for(i = 0;i < N - 1;i++)
   {
		//each loop to find the max or the min;
		for(j = i + 1;j < N;j++)
		{
			if(tosort[j] < tosort[j-1])		//从小到大排列
			{
				temp = tosort[j];
				tosort[j] = tosort[j-1];
				tosort[j-1] = temp;
			}
		}
	}
	
	//out
	for(i = 0;i < N;i++)
		cout<<tosort[i]<<endl;
	return 0;
}

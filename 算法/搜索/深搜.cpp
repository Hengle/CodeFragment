#include <iostream>
#include <time.h>
#include <stdlib.h>
using namespace std;

struct Node                       /* 图顶点结构定义     */
{
   int vertex;                    /* 顶点数据信息       */
   Node *left;         			/* 指下一顶点的指标   */
   Node *right;
};

Node *head = NULL;
int tofind;
int steps = 0;
bool isfound = false;

void insert(int val)
{
	if(head == NULL)
	{
		head = (Node*)malloc(sizeof(Node));
		head->vertex = val;
		head->left = NULL;
		head->right = NULL;
	}
	else
	{
		Node* temp = (Node*)malloc(sizeof(Node));
		temp->vertex = val;
		temp->left = NULL;
		temp->right = NULL;
		
		Node* loopvar = head;
		while(true)
		{
			if(loopvar->vertex < val)
			{
				if(loopvar->right == NULL)
				{
					loopvar->right = temp;
					break;
				}
				else
					loopvar = loopvar->right;
			}
			else if(loopvar->vertex == val)
				break;
			else
			{
				if(loopvar->left == NULL)
				{
					loopvar->left = temp;
					break;
				}
				else
					loopvar = loopvar->left;
			}
		}	//end while
	}		//end else
}

/**********************  图的深度优先搜寻法********************/
void recurive_dfs(Node* root)
{
	if(isfound == true)
		return;
	if(root == NULL)
		return;
	steps++;
	cout<<"Traversal:"<<root->vertex;
	if(root->vertex == tofind)
		isfound = true;
	else if(root->vertex < tofind)
	{
		cout<<"\tturn right!"<<endl;
		recurive_dfs(root->right);
	}
	else
	{		
		cout<<"\tturn left!"<<endl;
		recurive_dfs(root->left);
	}
}

/****************************** 主程序******************************/
int main()
{
   int n,m,i;
   
   srand(time(NULL));
   cout << "请输入数据范围：";
   cin >> n;
   do
	{
		cout << "请输入要查找的数(1-n):";
		cin >> m;
	}while(m < 1 || m > n);
	
	for(int i = 1;i <= n;i++)
		insert(rand() % n);
	
	tofind = m;
	recurive_dfs(head);
	cout << "\nSteps:"<<steps<<"\tResult:";
	if(isfound == true)
		cout<<"found"<<endl;
	else
		cout<<"not found"<<endl;
	return 0;
}
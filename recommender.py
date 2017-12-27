import numpy
import math
from itertools import izip

class Table(dict):
    
    def __init__(self):
        self.value_indices = {}
    
    def set(self, i, j, v):
        self[(i, j)] = v
        if i in self.value_indices:
            self.value_indices[i].add(j)
        else:
            self.value_indices[i] = set([j])
        
    def read(self, i, j):
        return self.get((i, j), None)
    
    def hasValues(self, i):
        idx = self.value_indices.get(i, None)
        return idx





T = Table()
#f = open('data/u1.base', 'r')





def importer(f,T):
    for l in f.readlines()[:100000]:
        l = l.split('\t')
        userid = int(l[0])
        movieid = int(l[1])
        rating = float(l[2])
        #print userid, movieid, rating
        T.set(userid, movieid, rating)

def averagecalc(T):
    it = sorted(T.items())
    #print len(it)
    sums= {}
    counts= {}
    for i in it:
        #print i
        user=i[0][0]
        rating=i[1]
        if user in sums:
            sums[user]= sums[user]+rating
            counts[user]= counts[user]+1
        else:
            sums[user]= rating
            counts[user]=1

    sumlist=sorted(sums.items())
    averages={}
    for user in sumlist:
        averages[user[0]]=sums[user[0]]/counts[user[0]]
    return averages





def predict(user, book, averages, T):

    userId = user
    v1=T.hasValues(userId)
    #print len(v1)
    #print('NOW SIMILARITIES!!')
    similarusers={}

    for j in sorted(averages.items()):
        simId = j[0]
        v2 = T.hasValues(simId)
        if userId != j[0]:

            myuser=[]
            simuser=[]
            similarity=0
            overlap = v1.intersection(v2)
            for i in overlap:
                #  print 'col {}: '.format(i), T.read(2, i), T.read(1, i)
                myuser.append(T.read(userId, i) - averages[userId])
                simuser.append(T.read(simId,i)- averages[simId])

            myuserdot=numpy.array(myuser)
            simuserdot=numpy.array(simuser)
            dividend= numpy.dot(myuserdot.T, simuserdot)
            divider= math.sqrt(numpy.dot(myuserdot.T, myuserdot))*math.sqrt(numpy.dot(simuserdot.T, simuserdot))
            if divider!=0:
                similarity= dividend/divider

            if math.fabs(similarity)>0.5: #and float(len(overlap))/float(len(v1))>0.05:
                #print len(overlap)
                #print "%.3f "%similarity +' with intersection; '+ str(overlap)
                similarusers[simId]=similarity
                if len(similarusers)>5:
                    break

    for simus in similarusers.keys():
        sorted_simus = sorted(similarusers[simus])


    prediction = averages[userId]
    simeff=0
    simsum=0
    print similarusers.keys()
    for simus in similarusers.keys():
        simeff= simeff+ similarusers[simus]*(T.read(simus,book)-averages[simus])
        simsum= simsum+abs(similarusers[simus])
    if simsum!=0:
        prediction = prediction + simeff/simsum
    #print 'Prediction for user ' + str(userId) + ' and movie ' + str(movie) + ': ' + str(round(prediction))
    #print 'Real value: ' + str(T.read(userId, movie))
    return round(prediction)

def testline(line):
    error=0
    count=0
    throughput=0
    line=line.split('\t')
    user=int(line[0])
    movie= int(line[1])
    #moviesrated= T.hasValues(user)
    #count=count+1
    prediction=predict(user, movie, averages, T)
    newline = str(user)+'\t'+ str(movie)+'\t'+ str(int(prediction))+'\n'
    #print newline
    return newline
    # error = error+ (difference*difference)
    # throughput= error/count
    # print 'user '+str(u)+' '+ str(throughput)

    

def createpfile(tf,ptf,T):
    for line in tf.readlines():
        ptf.write(testline(line))


for i in range(1,6):
    basef = 'data/u' + str(i) + '.base'
    testf = 'data/u'+str(i)+'.test'
    testpredf = 'data/u'+str(i)+'.test.Prediction'
    basepredf =  'data/u'+str(i)+'.base.Prediction'
    #print basef

    #basef =
    #testf =
    T=Table()
    bf = open(basef,'r')
    importer(bf,T)
    averages = averagecalc(T)
    bf.close()

    # bf=open(basef,'r')
    # pbf=open(basepredf,'w')
    # createpfile(bf, pbf, T)
    # bf.close()
    # msetest= compare(basef,basepredf)
    # print "Base" + str(i) + " MSE; " + str(float(msetest))

    ptf= open(testpredf,'w')
    tf= open(testf,'r')
    createpfile(tf,ptf,T)
    tf.close()

    
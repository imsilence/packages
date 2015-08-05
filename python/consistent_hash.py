#!/usr/bin/env python
#encoding: utf-8
import hashlib

class SelfException(Exception):
    pass


class ConsistentHash(object):
    def __init__(self):
        self._hash_func = Hasher.hash_md5       #hash算法回调函数
        self._position2target = {}              #虚拟节点与target对应表
        self._target2position = {}              #target于虚拟节点对应表
        self._target_count = 0
        self._replicas = 30                     #虚拟节点数量
        self._is_sorted = False

    def add_target(self, target, weight=1):
        '''
                                        添加target节点
        '''
        if target in self._target2position:
            raise SelfException('alreay exists target:%s' % target)
        
        for _i in xrange(self._replicas * weight):
            '''
                                                    复制虚拟节点
            '''
            
            _position = self._hash_func('%s#%d' % (target, _i))
            
            self._position2target[_position] = target
            self._target2position.setdefault(target, [])
            self._target2position[target].append(_position)
            
        self._target_count += 1
        self._is_sorted = False
    
        return self
    
    def add_targets(self, targets, weight=1):
        for target in targets:
            self.add_target(target, weight)
            
        return self
    
    def remove_target(self, target):
        '''
                                        移除target节点
        '''
        
        if target not in self._target2position:
            raise SelfException('not found target:%s' % target)
        
        for _position in self._target2position.get(target):
            del self._position2target[_position]
        
        del self._target2position[target]
        
        self._target_count -= 1
        
        return self
    
    def lookup(self, resource):
        _targets = self.lookup_list(resource)
        
        if len(_targets) == 0:
            raise SelfException('not mapping to target')
        
        return _targets[0]
    
    def lookup_list(self, resource, resource_cnt=1):
        
        self._sort_targets()
        
        _targets = []
        _position_resource = self._hash_func(resource)
        _found = False
        _found_count = 0
        
        '''
                                         从虚拟节点中查找对应target节点
        '''
        for _position, _target in self._position2target.iteritems():
            
            if _found_count >= resource_cnt or _found_count >= self._target_count:
                break
            
            if not _found and _position > _position_resource:
                _found = True
                
            if _found and _target not in _targets:
                _targets.append(_target)
                _found_count += 1
                
        '''
                                        当匹配的虚拟节点在环的末尾时，不够需要查询的数量时从环头再次遍历
        '''
        for _position, _target in self._position2target.iteritems():
            if _found_count >= resource_cnt or _found_count >= self._target_count:
                break
            if _target not in _targets:
                _targets.append(_target)
                _found_count += 1
                
        return _targets
    
    def _sort_targets(self):
        '''
                                        对虚拟节点根据key进行排序
        '''
        if not self._is_sorted:
            self._is_sorted = True
            _p2t = self._position2target
            _temp = [(k, _p2t[k]) for k in sorted(_p2t.keys())]
            self._position2target = dict(_temp)
        
    
class Hasher(object):
    
    @staticmethod
    def hash_md5(s):
        _util = hashlib.md5()
        _util.update(s)
        return _util.hexdigest()[:8]
        

if __name__ == '__main__':
    _util = ConsistentHash()
    for i in xrange(0, 3):
        _util.add_target('target-%s' % i)
    print _util.lookup_list('a', 2)
    print _util.remove_target('target-0').lookup('a')

# Task2 — Отчет по метрикам

Дата: `2026-01-31 13:52:17`


### Статус кластера: kubectl config current-context (exit=0)

```
task2
```


### Статус кластера: kubectl get nodes -o wide (exit=0)

```
NAME    STATUS   ROLES           AGE     VERSION   INTERNAL-IP    EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION     CONTAINER-RUNTIME
task2   Ready    control-plane   4h17m   v1.34.0   192.168.58.2   <none>        Ubuntu 22.04.5 LTS   6.12.65-linuxkit   docker://28.4.0
```


### Статус кластера: kubectl get pods -n kube-system -l k8s-app=metrics-server -o wide (exit=0)

```
NAME                              READY   STATUS    RESTARTS   AGE     IP            NODE    NOMINATED NODE   READINESS GATES
metrics-server-85b7d694d7-gr9wd   1/1     Running   0          3h37m   10.244.0.13   task2   <none>           <none>
```


### Статус кластера: kubectl get apiservice v1beta1.metrics.k8s.io -o wide (exit=0)

```
NAME                     SERVICE                      AVAILABLE   AGE
v1beta1.metrics.k8s.io   kube-system/metrics-server   True        3h37m
```


### Статус приложения: kubectl get deploy,svc,pods -l app=scaletestapp -o wide (exit=0)

```
NAME                           READY   UP-TO-DATE   AVAILABLE   AGE    CONTAINERS     IMAGES                                         SELECTOR
deployment.apps/scaletestapp   2/2     2            2           4h6m   scaletestapp   ghcr.io/yandex-practicum/scaletestapp:latest   app=scaletestapp

NAME                   TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE    SELECTOR
service/scaletestapp   NodePort   10.107.225.85   <none>        8080:31337/TCP   4h6m   app=scaletestapp

NAME                               READY   STATUS    RESTARTS   AGE    IP            NODE    NOMINATED NODE   READINESS GATES
pod/scaletestapp-65c6bc858-qmqcq   1/1     Running   0          2m9s   10.244.0.21   task2   <none>           <none>
pod/scaletestapp-65c6bc858-tl2hf   1/1     Running   0          11m    10.244.0.17   task2   <none>           <none>
```


### Статус приложения: kubectl get hpa -o wide (exit=0)

```
NAME               REFERENCE                 TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
scaletestapp-rps   Deployment/scaletestapp   300m/20   1         10        2          3m9s
```


### HPA memory: kubectl describe hpa scaletestapp-memory (exit=1)

```
Error from server (NotFound): horizontalpodautoscalers.autoscaling "scaletestapp-memory" not found
```


### HPA RPS: kubectl describe hpa scaletestapp-rps (exit=0)

```
Name:                                  scaletestapp-rps
Namespace:                             default
Labels:                                <none>
Annotations:                           <none>
CreationTimestamp:                     Sat, 31 Jan 2026 13:49:08 +0100
Reference:                             Deployment/scaletestapp
Metrics:                               ( current / target )
  "http_requests_per_second" on pods:  300m / 20
Min replicas:                          1
Max replicas:                          10
Behavior:
  Scale Up:
    Stabilization Window: 0 seconds
    Select Policy: Max
    Policies:
      - Type: Percent  Value: 100  Period: 60 seconds
      - Type: Pods     Value: 4    Period: 60 seconds
  Scale Down:
    Stabilization Window: 300 seconds
    Select Policy: Max
    Policies:
      - Type: Percent  Value: 50  Period: 60 seconds
Deployment pods:       2 current / 2 desired
Conditions:
  Type            Status  Reason               Message
  ----            ------  ------               -------
  AbleToScale     True    ScaleDownStabilized  recent recommendations were higher than current one, applying the highest recent recommendation
  ScalingActive   True    ValidMetricFound     the HPA was able to successfully calculate a replica count from pods metric http_requests_per_second
  ScalingLimited  False   DesiredWithinRange   the desired count is within the acceptable range
Events:
  Type    Reason             Age   From                       Message
  ----    ------             ----  ----                       -------
  Normal  SuccessfulRescale  2m9s  horizontal-pod-autoscaler  New size: 2; reason: pods metric http_requests_per_second above target
```


### Метрики ресурса: kubectl top pods (exit=0)

```
NAME                           CPU(cores)   MEMORY(bytes)   
scaletestapp-65c6bc858-qmqcq   1m           11Mi            
scaletestapp-65c6bc858-tl2hf   2m           21Mi
```


### Метрики ресурса: kubectl top pods -n default (exit=0)

```
NAME                           CPU(cores)   MEMORY(bytes)   
scaletestapp-65c6bc858-qmqcq   1m           11Mi            
scaletestapp-65c6bc858-tl2hf   2m           21Mi
```


### Custom Metrics API (list)

```
{"kind":"APIResourceList","apiVersion":"v1","groupVersion":"custom.metrics.k8s.io/v1beta1","resources":[{"name":"namespaces/http_requests_per_second","singularName":"","namespaced":false,"kind":"MetricValueList","verbs":["get"]},{"name":"pods/http_requests_per_second","singularName":"","namespaced":true,"kind":"MetricValueList","verbs":["get"]}]}
```


### Custom Metric http_requests_per_second

```
items=2, sample=http_requests_per_second=300m
```


### Prometheus targets

```
targets_total=19, targets_up=16, sample_labels=[{'container': 'scaletestapp', 'endpoint': 'http', 'instance': '10.244.0.17:8080', 'job': 'scaletestapp', 'namespace': 'default', 'pod': 'scaletestapp-65c6bc858-tl2hf', 'service': 'scaletestapp'}, {'container': 'scaletestapp', 'endpoint': 'http', 'instance': '10.244.0.21:8080', 'job': 'scaletestapp', 'namespace': 'default', 'pod': 'scaletestapp-65c6bc858-qmqcq', 'service': 'scaletestapp'}, {'container': 'alertmanager', 'endpoint': 'http-web', 'instance': '10.244.0.8:9093', 'job': 'kube-prometheus-stack-alertmanager', 'namespace': 'monitoring', 'pod': 'alertmanager-kube-prometheus-stack-alertmanager-0', 'service': 'kube-prometheus-stack-alertmanager'}]
```


### Prometheus query http_requests_total

```
metric={'__name__': 'http_requests_total', 'container': 'scaletestapp', 'endpoint': 'http', 'instance': '10.244.0.17:8080', 'job': 'scaletestapp', 'namespace': 'default', 'pod': 'scaletestapp-65c6bc858-tl2hf', 'service': 'scaletestapp'}, value=[1769863937.768, '9952']
```


## Locust (memory)

Type=, Name=Aggregated, Requests=None, Failures=None, RPS=48.079312788884806, Avg=None, Min=None, Max=None

## Locust (RPS)

Type=, Name=Aggregated, Requests=None, Failures=None, RPS=33.1050404022569, Avg=None, Min=None, Max=None
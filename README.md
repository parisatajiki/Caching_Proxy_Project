# Caching Proxy CLI

A simple **Caching Proxy Server** built in Python using `http.server`.  
It forwards requests to an origin server and caches responses to improve performance.  

https://roadmap.sh/projects/caching-server


---


## **Features**

- Forward GET requests to the origin server
- Cache responses in memory
- Detect if response comes from cache or origin server
- Clear cache using CLI option

---

## **Requirements**

- Python 3.x  
No external packages required, uses standard Python libraries:  
`http.server`, `socketserver`, `urllib`, `argparse`, `sys`

---

## **Usage**

1. **Run the caching proxy server:**

```bash
python main.py --port 3000 --origin http://dummyjson.com
```
2. **Test with curl:
```bash
curl -i http://localhost:3000/products
```
First request → X-Cache: MISS
Second request → X-Cache: HIT

2. **Clear cache:
```bash
python main.py --clear-cache
```



package main

import (
	"bufio"
	"fmt"
	"github.com/go-martini/martini"
	"github.com/martini-contrib/render"
	"io"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
	"os/exec"
	"sort"
	"strconv"
	"strings"
	"sync"
)

var filemap = make(map[string]int)
var leafnodemap = make(map[int][]string)
var serveraddress [16]string

func main() {

	serveraddress = [16]string{"http://54.148.202.32:8080/LeafNodeWebService/search", "http://54.149.97.128:8080/LeafNodeWebService/search", "http://54.149.97.151:8080/LeafNodeWebService/search", "http://54.149.95.156:8080/LeafNodeWebService/search", "http://54.149.97.100:8080/LeafNodeWebService/search", "http://54.149.97.139:8080/LeafNodeWebService/search", "http://54.149.97.118:8080/LeafNodeWebService/search", "http://54.149.97.133:8080/LeafNodeWebService/search", "http://54.149.97.114:8080/LeafNodeWebService/search", "http://54.149.97.152:8080/LeafNodeWebService/search", "http://54.69.196.15:8080/LeafNodeWebService/search", "http://54.148.190.213:8080/LeafNodeWebService/search", "http://54.148.45.65:8080/LeafNodeWebService/search", "http://54.148.89.118:8080/LeafNodeWebService/search", "http://54.148.190.81:8080/LeafNodeWebService/search", "http://54.69.164.48:8080/LeafNodeWebService/search"}
	m := martini.Classic()
	m.Use(render.Renderer())

	m.Get("/", func(r render.Render) {
		r.HTML(200, "index", nil)
	})

	m.Post("/uploadfile", uploadHandler)

	m.Run()

}

func uploadHandler(w http.ResponseWriter, r *http.Request, rend render.Render) {

	var wg sync.WaitGroup
	file, header, err := r.FormFile("file")
	defer file.Close()

	if err != nil {
		fmt.Fprintln(w, err)
		return
	}

	out, err := os.Create("/datauploads/" + header.Filename)
	if err != nil {
		fmt.Fprintf(w, "Unable to create the file for writing. Check your write access privilege")
		return
	}

	defer out.Close()

	// write the content from POST to the file
	_, err = io.Copy(out, file)
	if err != nil {
		fmt.Fprintln(w, err)

	}

	cmd := exec.Command("python", "sift.py", "/datauploads/"+header.Filename)

	stdout, err := cmd.StdoutPipe()

	cmd.Start()

	// read command's stdout line by line
	in := bufio.NewScanner(stdout)

	for in.Scan() {
		fmt.Println("run reqeuest start ", in.Text())

		text := in.Text()

		siftstring := strings.Split(text, "+")

		node1, _ := strconv.ParseFloat(siftstring[104], 64)
		node2, _ := strconv.ParseFloat(siftstring[16], 64)
		node3, _ := strconv.ParseFloat(siftstring[8], 64)
		node4, _ := strconv.ParseFloat(siftstring[80], 64)
		node5, _ := strconv.ParseFloat(siftstring[112], 64)
		node6, _ := strconv.ParseFloat(siftstring[48], 64)
		node7, _ := strconv.ParseFloat(siftstring[112], 64)
		node8, _ := strconv.ParseFloat(siftstring[83], 64)
		node9, _ := strconv.ParseFloat(siftstring[76], 64)
		node10, _ := strconv.ParseFloat(siftstring[80], 64)
		node11, _ := strconv.ParseFloat(siftstring[44], 64)
		node12, _ := strconv.ParseFloat(siftstring[84], 64)
		node13, _ := strconv.ParseFloat(siftstring[16], 64)
		node14, _ := strconv.ParseFloat(siftstring[52], 64)
		node15, _ := strconv.ParseFloat(siftstring[16], 64)

		if node1 <= 62.395731654 {

			if node2 <= 58.3006844724 {

				if node4 <= 77.5953237046 {

					if node8 <= 62.1624811219 {

						leafnodemap[16] = append(leafnodemap[16], text)

					} else {

						leafnodemap[17] = append(leafnodemap[17], text)
					}
				} else {

					if node9 <= 46.356839383 {

						leafnodemap[18] = append(leafnodemap[18], text)

					} else {

						leafnodemap[19] = append(leafnodemap[19], text)
					}
				}
			} else {
				if node5 <= 59.925128547 {

					if node10 <= 87.5045001727 {

						leafnodemap[20] = append(leafnodemap[20], text)

					} else {

						leafnodemap[21] = append(leafnodemap[21], text)
					}
				} else {

					if node11 <= 57.314103421 {

						leafnodemap[22] = append(leafnodemap[22], text)

					} else {

						leafnodemap[23] = append(leafnodemap[23], text)
					}
				}

			}

		} else {
			if node3 <= 80.1688231564 {

				if node6 <= 81.8823925808 {

					if node12 <= 53.0322435683 {

						leafnodemap[24] = append(leafnodemap[24], text)

					} else {

						leafnodemap[25] = append(leafnodemap[25], text)
					}
				} else {

					if node13 <= 74.2278004283 {

						leafnodemap[26] = append(leafnodemap[26], text)

					} else {

						leafnodemap[27] = append(leafnodemap[27], text)
					}
				}
			} else {
				if node7 <= 84.9359341494 {

					if node14 <= 52.2214200302 {

						leafnodemap[28] = append(leafnodemap[28], text)

					} else {

						leafnodemap[29] = append(leafnodemap[29], text)
					}
				} else {

					if node15 <= 110.164291138 {

						leafnodemap[30] = append(leafnodemap[30], text)

					} else {

						leafnodemap[31] = append(leafnodemap[31], text)
					}
				}

			}

		}
	}

	for i := 16; i < 32; i++ {
		wg.Add(1)

		go rungets(&wg, i)

	}

	wg.Wait()
	var values []int
	for k, v := range filemap {
		fmt.Println("key value pair", k, v)
		values = append(values, v)
	}
	sort.Ints(values)
	var topfilename string
	fmt.Println("top value", values[len(values)-1])
	top := values[len(values)-1]
	top2 := values[len(values)-2]
	top3 := values[len(values)-3]
	top4 := values[len(values)-4]
	top5 := values[len(values)-5]

	for k, v := range filemap {
		if v == top {
			topfilename = k
		}

		if v == top2 {
			fmt.Println("top 2 value", v, k)
		}
		if v == top3 {
			fmt.Println("top 3 value", v, k)
		}

		if v == top4 {
			fmt.Println("top 4 value", v, k)

		}
		if v == top5 {
			fmt.Println("top 5 value", v, k)

		}

	}

	filemap = make(map[string]int)

	rend.JSON(200, map[string]interface{}{"filename": topfilename})

}

func rungets(wg *sync.WaitGroup, node int) {

	fmt.Println("Post reqeust start ")
	// write each line to your log, or anything you need

	text := strings.Join(leafnodemap[node], ";")

	values := make(url.Values)
	values.Set("param1", text)
	resp, err := http.PostForm(serveraddress[node-16], values)

	fmt.Println("from rungets ", text)

	defer resp.Body.Close()
	contents, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("%s", err)

	}
	fmt.Printf("%s\n", string(contents))
	key := string(contents)

	fmt.Println(key)
	imagenames := strings.Split(key, " ")

	for _, value := range imagenames {
		insert(value)
	}

	fmt.Println("get reqeuest end ")

	wg.Done()
	return
}

func insert(key string) {

	v, ok := filemap[key]
	if ok {
		//ctemp.disconnect<-1000
		filemap[key] = v + 1
	} else {
		filemap[key] = 1

	}

}

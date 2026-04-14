export namespace main {
	
	export class Entry {
	    Id: number;
	    Username: string;
	    Email: string;
	    Password: string;
	
	    static createFrom(source: any = {}) {
	        return new Entry(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.Id = source["Id"];
	        this.Username = source["Username"];
	        this.Email = source["Email"];
	        this.Password = source["Password"];
	    }
	}

}


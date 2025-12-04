package vm

type Network interface {
	Id 			int
	Bridge		string 	
	Firewall 	bool
	Link_down	bool
	Model		string
}

type Disk interface {
	
}

type CloudInit interface {

}

type CPUFlags enum {

}

type CPU interface {
	affinity	string
	cores		int
	limit		int
	numa		bool
	sockets		int
	type		string
	units		int
	vcores		int
	flags		[]CPUFlags
}

type vm struct{
	Name				string
	Id					int
	TargetNode			string
	Agent				bool
	Boot				string
	Network				[]Networks
	Description			string
	StartAtNodeBoot		bool
	ProtectFromDeletion	bool
	Bootdisk			string
	Pxe					bool
	Clone				string
	CloneId				int
	FullClone			bool
	HAState				string
	HAGroup				string
	QemuOS				string
	Memory				string
	MemoryBallon		string
	Hotplug				[]string
	SCSIHW				string
	Pool				string
	Tags				[]string
	OSType				string
	CloudInit			CloudInit
	CPU					CPU
}
